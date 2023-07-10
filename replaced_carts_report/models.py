from typing import Final, Optional

from django.db import models

_GOOD: Final = 'Good'
_BAD: Final = 'Bad'


class current_seal_state_for_front(models.Model):
    # current_pallet_state = models.ForeignKey(
    #     current_pallet_state,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="seal_state_for_front",
    # )
    # pallet = models.ForeignKey(
    #     pallets,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="seal_states_for_front",
    # )
    time = models.DateTimeField(blank=True, null=True)
    number = models.CharField(max_length=3, blank=True, null=True)
 
    path_cam1_left = models.CharField(max_length=512, blank=True, null=True)
    path_cam1_right = models.CharField(max_length=512, blank=True, null=True)
    path_cam2_left = models.CharField(max_length=512, blank=True, null=True)
    path_cam2_right = models.CharField(max_length=512, blank=True, null=True)
 
    state_cam1_left = models.CharField(max_length=100, blank=True, null=True)
    state_cam1_right = models.CharField(max_length=100, blank=True, null=True)
    state_cam2_left = models.CharField(max_length=100, blank=True, null=True)
    state_cam2_right = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "app_current_seal_state_for_front"


class current_bolts_state_for_front(models.Model):
    # current_pallet_state = models.ForeignKey(
    #     current_pallet_state,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="bolts_state_for_front",
    # )
    # pallet = models.ForeignKey(
    #     pallets,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name="bolts_states_for_front",
    # )
    time = models.DateTimeField(blank=True, null=True)
    number = models.CharField(max_length=3, blank=True, null=True)
 
    path_cam1 = models.CharField(max_length=512, blank=True, null=True)
    path_cam2 = models.CharField(max_length=512, blank=True, null=True)
 
    state_cam1 = models.CharField(max_length=100, blank=True, null=True)
    state_cam2 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "app_current_bolts_state_for_front"


class CartReplacement(models.Model):
    """Agglomerate cart replacement record."""

    prev_no = models.IntegerField(
        db_column='no',
        help_text='The number of the replaced (previous) cart.',
    )
    prev_cart_detected = models.DateTimeField(
        db_column='time',
        help_text='Time when replaced (previous) cart was last detected.',
    )
    new_no = models.IntegerField(
        db_column='replace_no',
        help_text='The number of the replacing (new) cart.',
    )
    created = models.DateTimeField(help_text='Record creation time.')

    class Meta:
        managed = False
        db_table = 'app_replacedcarts'

    def __str__(self) -> str:
        """All django models should have this method."""
        return 'id: {0}, prev no: {1}, new no: {2}, created: {3}'.format(
            self.id, 
            self.prev_no, 
            self.new_no,
            self.created,
        )


class CartReplacementReason(models.Model):
    """Possible reason for agglomerate cart replacement."""

    prev_no = models.IntegerField(
        help_text='The number of the replaced (previous) cart. Duplicates CartReplacement model `prev_no`.',
    )
    new_no = models.IntegerField(
        help_text='The number of the replacing (new) cart. Duplicates CartReplacement model `new_no`.',
    )    
    replacement = models.OneToOneField(
        CartReplacement,
        on_delete=models.CASCADE,
        null=False,
        related_name='cart_replacement_reason',
        help_text='Cart replacement record.',
    )

    bad_seal_cam1_left = models.ForeignKey(
        current_seal_state_for_front,
        on_delete=models.PROTECT,
        null=True,
        related_name='cam1_left_cart_replacement_reasons',
        help_text='Bad seal state record by left cam1 observation. Null if left cam1 state is good.',
    )
    bad_seal_cam1_right = models.ForeignKey(
        current_seal_state_for_front,
        on_delete=models.PROTECT,
        null=True,
        related_name='cam1_right_cart_replacement_reasons',
        help_text='Bad seal state record by right cam1 observation. Null if right cam1 state is good.',
    )
    bad_seal_cam2_left = models.ForeignKey(
        current_seal_state_for_front,
        on_delete=models.PROTECT,
        null=True,
        related_name='cam2_left_cart_replacement_reasons',
        help_text='Bad seal state record by left cam2 observation. Null if left cam2 state is good.',
    )
    bad_seal_cam2_right = models.ForeignKey(
        current_seal_state_for_front,
        on_delete=models.PROTECT,
        null=True,
        related_name='cam2_right_cart_replacement_reasons',
        help_text='Bad seal state record by right cam2 observation. Null if right cam2 state is good.',
    )

    bad_bolt_cam1 = models.ForeignKey(
        current_bolts_state_for_front,
        on_delete=models.PROTECT,
        null=True,
        related_name='cam1_cart_replacement_reasons',
        help_text='Bad bolt state record by cam1 observation. Null if cam1 state is good.',
    )
    bad_bolt_cam2 = models.ForeignKey(
        current_bolts_state_for_front,
        on_delete=models.PROTECT,
        null=True,
        related_name='cam2_cart_replacement_reasons',
        help_text='Bad bolt state record by cam2 observation. Null if cam2 state is good.',
    )

    def __str__(self) -> str:
        """All django models should have this method."""
        return 'id: {0}, prev no: {1}, new no: {2}, has replacement reason: {3}'.format(
            self.id, 
            self.prev_no, 
            self.new_no,
            any(bad_state_id is not None for bad_state_id in (
                self.bad_seal_cam1_left_id,
                self.bad_seal_cam1_right_id,
                self.bad_seal_cam2_left_id,
                self.bad_seal_cam2_right_id,
                self.bad_bolt_cam1_id,
                self.bad_bolt_cam2_id,
            )),
        )
