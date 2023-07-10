from datetime import date
from typing import Final

from django.db import connection

from .models import (
    CartReplacementReason,
    _BAD,
)


_RAW_SQL: Final = '''
with replacements_tmp as (
	select 
		id,
		(
			SELECT 
				prev_replacements.id 
			FROM 
				app_replacedcarts as prev_replacements
			WHERE (prev_replacements.created < (replacements.created) 
				AND prev_replacements.replace_no = replacements."no")
			ORDER BY created DESC 
			LIMIT 1
		) AS prev_cart_replacement,
		"no" as prev_no,
		"time" as prev_cart_detected_at,
		replace_no as new_no,
		created as replaced_up_to
	from app_replacedcarts as replacements
	where (created AT TIME ZONE 'UTC')::date between %s AND %s
), replacements as (
	select 
		replacements_tmp.*,
		prev_replacements.created as prev_replaced_up_to
	from replacements_tmp 
		left join app_replacedcarts as prev_replacements
	on
		replacements_tmp.prev_cart_replacement = prev_replacements.id
), reason_ids as (
	select 
		id as replacement_id,
		prev_no,
		new_no,
		prev_replaced_up_to,
		replaced_up_to,
		(
			select id 
			from app_current_bolts_state_for_front as bolts
			where
				"number" = prev_no::text
				and bolts."time" between prev_replaced_up_to and replaced_up_to
				and (state_cam1 = '{0}' or state_cam2 = '{0}')
			ORDER BY bolts."time" DESC 
			LIMIT 1
		) as bad_bolt_id,
		(
			select id 
			from app_current_seal_state_for_front as seals
			where
				"number" = prev_no::text
				and seals."time" between prev_replaced_up_to and replaced_up_to
				and (
					state_cam1_left = '{0}' 
					or state_cam1_right = '{0}' 
					or state_cam2_left = '{0}'
					or state_cam2_right = '{0}'
				)
			ORDER BY seals."time" DESC 
			LIMIT 1
		) as bad_seal_id
	from replacements
), reasons as (
	select
		reason_ids.replacement_id,
		reason_ids.prev_no,
		reason_ids.new_no,
		reason_ids.prev_replaced_up_to,
		reason_ids.replaced_up_to,
		bolts."time" as bad_bolt_time, 
		seals."time" as bad_seal_time, 
		case when bolts.state_cam1 = '{0}' then bolts.id end bad_bolt_cam1_id,
		case when bolts.state_cam2 = '{0}' then bolts.id end bad_bolt_cam2_id,
		case when seals.state_cam1_left = '{0}' then seals.id end bad_seal_cam1_left_id,
		case when seals.state_cam1_right = '{0}' then seals.id end bad_seal_cam1_right_id,
		case when seals.state_cam2_left = '{0}' then seals.id end bad_seal_cam2_left_id,
		case when seals.state_cam2_right = '{0}' then seals.id end bad_seal_cam2_right_id
	from 
		reason_ids
		left join app_current_bolts_state_for_front as bolts
			on reason_ids.bad_bolt_id = bolts.id
		left join app_current_seal_state_for_front as seals
			on reason_ids.bad_seal_id = seals.id
)
select 
    replacement_id,
    prev_no,
    new_no,
    bad_bolt_cam1_id,
    bad_bolt_cam2_id,
    bad_seal_cam1_left_id,
    bad_seal_cam1_right_id,
    bad_seal_cam2_left_id,
    bad_seal_cam2_right_id
from reasons
order by replaced_up_to
'''.format(_BAD)


def fill_replacement_reasons(date_from: date = date.today(), date_to: date = date.today()):
    """Fill replacement reasons."""
    with connection.cursor() as cursor:
        cursor.execute(_RAW_SQL, (date_from, date_to))
        field_name = tuple(col.name for col in cursor.description)
        reasons = []
        for row in cursor.fetchall():
            fields = {field_name[i]: field_val for i, field_val in enumerate(row)}
            reasons.append(CartReplacementReason(**fields))
        return CartReplacementReason.objects.bulk_create(reasons, ignore_conflicts=True)
