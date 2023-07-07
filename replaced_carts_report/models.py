from django.db import models


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
