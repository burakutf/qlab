from django.db.models import TextChoices

# TODO minimal viewlere permission vermedim gerekli olursa koy
class PermissionChoice(TextChoices):
    USER_CREATE = 'user.create', ('KULLANICI OLUŞTUR')
    USER_VIEW = 'user.view', ('KULLANICI GÖRÜNTÜLE')
    USER_UPDATE = 'user.update', ('KULLANICI GÜNCELLE')
    USER_DELETE = 'user.destroy', ('KULLANICI SİL')

    GROUP_CREATE = 'group.create', ('GRUP OLUŞTUR')
    GROUP_VIEW = 'group.view', ('GRUP GÖRÜNTÜLE')
    GROUP_UPDATE = 'group.update', ('GRUP GÜNCELLE')
    GROUP_DELETE = 'group.destroy', ('GRUP SİL')

    VEHICLE_CREATE = 'vehicle.create', ('ARAÇ OLUŞTUR')
    VEHICLE_VIEW = 'vehicle.view', ('ARAÇ GÖRÜNTÜLE')
    VEHICLE_UPDATE = 'vehicle.update', ('ARAÇ GÜNCELLE')
    VEHICLE_DELETE = 'vehicle.destroy', ('ARAÇ SİL')

    COMPANY_CREATE = 'company.create', ('FİRMA OLUŞTUR')
    COMPANY_VIEW = 'company.view', ('FİRMA GÖRÜNTÜLE')
    COMPANY_UPDATE = 'company.update', ('FİRMA GÜNCELLE')
    COMPANY_DELETE = 'company.destroy', ('FİRMA SİL')

    METHOD_CREATE = 'method.create', ('METOT OLUŞTUR')
    METHOD_VIEW = 'method.view', ('METOT GÖRÜNTÜLE')
    METHOD_UPDATE = 'method.update', ('METOT GÜNCELLE')
    METHOD_DELETE = 'method.destroy', ('METOT SİL')

    PARAMETER_CREATE = 'parameter.create', ('PARAMETRE OLUŞTUR')
    PARAMETER_VIEW = 'parameter.view', ('PARAMETRE GÖRÜNTÜLE')
    PARAMETER_UPDATE = 'parameter.update', ('PARAMETRE GÜNCELLE')
    PARAMETER_DELETE = 'parameter.destroy', ('PARAMETRE SİL')

    DEVICE_CREATE = 'device.create', ('CİHAZ OLUŞTUR')
    DEVICE_VIEW = 'device.view', ('CİHAZ GÖRÜNTÜLE')
    DEVICE_UPDATE = 'device.update', ('CİHAZ GÜNCELLE')
    DEVICE_DELETE = 'device.destroy', ('CİHAZ SİL')

    DRAFT_CREATE = 'draft.create', ('TASLAK OLUŞTUR')
    DRAFT_VIEW = 'draft.view', ('TASLAK GÖRÜNTÜLE')
    DRAFT_UPDATE = 'draft.update', ('TASLAK GÜNCELLE')
    DRAFT_DELETE = 'draft.destroy', ('TASLAK SİL')

    PROPOSAL_CREATE = 'proposal_create', ('TEKLİF OLUŞTUR')
    PROPOSAL_UPDATE = 'proposal_update', ('TEKLİF GÜNCELLE')
    PROPOSAL_VIEW = 'proposal_view', ('TEKLİF GÖRÜNTÜLE')

    STATISTICS_VIEW = 'statistics.view', ('İSTATİSTİK GÖRÜNTÜLE')

    NOTE_CREATE = 'note.create', ('NOT OLUŞTUR')
    NOTE_VIEW = 'note.view', ('NOT GÖRÜNTÜLE')
    NOTE_UPDATE = 'note.update', ('NOT GÜNCELLE')
    NOTE_DELETE = 'note.destroy', ('NOT SİL')


ALL_PERMS = [perm for perm, x in PermissionChoice.choices]
PERMS_MAP = {perm: value for perm, value in PermissionChoice.choices}
