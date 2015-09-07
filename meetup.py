

from heat.engine import properties
from heat.engine import constraints
from heat.engine import resource


from mock import MagicMock


class SysAdmin(resource.Resource):

    PROPERTIES = (BEARD_LENGTH, GLASSES, FAVORITE_ANIMAL) = \
        ('beard_length', 'glasses', 'favorite_animal')

    properties_schema = {
        BEARD_LENGTH: properties.Schema(
            data_type=properties.Schema.INTEGER,
            description='The SysAdmins beard length (in mm)',
            required=True,
            default=2,
        ),
        GLASSES: properties.Schema(
            data_type=properties.Schema.BOOLEAN,
            description='Does the SysAdmin wear glasses?',
            required=False,
            default=True
        ),
        FAVORITE_ANIMAL: properties.Schema(
            data_type=properties.Schema.STRING,
            description='The Sysadmins favorite animal',
            required=True,
            default='Cats',
            constraints=[
                constraints.AllowedPattern('(Cat[s]?)')
            ],
            update_allowed=True
        )
    }

    ATTRIBUTES = (NAME, BEARD_LENGTH) = ('name', 'beard_length')

    attributes_schema = {
        NAME: 'the sysadmins name',
        BEARD_LENGTH: 'the sysadmins beard length'
    }

    @staticmethod
    def _get_hr():

        sysadmin = MagicMock()
        sysadmin.name = 'Chuck'
        sysadmin.beard_length = '25'
        sysadmin.uuid = '5274DBBE-56F2-4E2F-992E-D27728E5969A'
        sysadmin.favorite_animal = 'Cats'
        sysadmin.is_working = MagicMock()
        sysadmin.is_working.return_value = True
        sysadmin.send_on_vacations = MagicMock()
        sysadmin.send_on_vacations.return_value = True
        sysadmin.is_on_vacations = MagicMock()
        sysadmin.is_on_vacations.return_value = True
        sysadmin.call_to_get_back_asap = MagicMock()
        sysadmin.call_to_get_back_asap.return_value = True
        sysadmin.fire = MagicMock()
        sysadmin.fire.return_value = True
        sysadmin.is_fired = MagicMock()
        sysadmin.is_fired.return_value = True
        sysadmin.set_favorite_animal = MagicMock()
        sysadmin.set_favorite_animal.return_value = True
        sysadmin.call_to_get_back_asap = MagicMock()
        sysadmin.call_to_get_back_asap.return_value = True
        sysadmin.fire = MagicMock()
        sysadmin.fire.return_value = True
        sysadmin.is_fired = MagicMock()
        sysadmin.is_fired.return_value = True
        sysadmin.set_favorite_animal = MagicMock()
        sysadmin.set_favorite_animal.return_value = True

        hr = MagicMock()
        hr.get_sysadmin = MagicMock()
        hr.get_sysadmin.return_value = sysadmin
        hr.hire_sysadmin = MagicMock()
        hr.hire_sysadmin.return_value = sysadmin

        return hr

    def _resolve_attribute(self, attribute):

        hr = self._get_hr()

        sysadmin = hr.get_sysadmin(self.resource_id)
        if sysadmin:
            if attribute == 'name':
                return sysadmin.name
            if attribute == 'beard_length':
                return sysadmin.beard_length
            return getattr(sysadmin, attribute)
        return None

    def handle_create(self):

        hr = self._get_hr()

        beard_length = self.properties.get(self.BEARD_LENGTH)
        glasses = self.properties.get(self.GLASSES)
        favorite_animal = self.properties.get(self.FAVORITE_ANIMAL)

        sysadmin = hr.hire_sysadmin(beard_length=beard_length,
                                    glasses=glasses,
                                    favorite_animal=favorite_animal)

        self.resource_id_set(sysadmin.uuid)

        return sysadmin.uuid

    def check_create_complete(self, sysadmin_uuid):

        hr = self._get_hr()

        sysadmin = hr.get_sysadmin(sysadmin_uuid)

        return sysadmin.is_working()

    def handle_suspend(self):

        hr = self._get_hr()

        sysadmin = hr.get_sysadmin(self.resource_id)

        sysadmin.send_on_vacations()

    def check_suspend_complete(self, sysadmin_uuid):
        hr = self._get_hr()

        sysadmin = hr.get_sysadmin(sysadmin_uuid)

        return sysadmin.is_on_vacations()

    def handle_resume(self):

        hr = self._get_hr()

        sysadmin = hr.get_sysadmin(self.resource_id)

        sysadmin.call_to_get_back_asap()

    def check_resume_complete(self, sysadmin_uuid):

        hr = self._get_hr()

        sysadmin = hr.get_sysadmin(sysadmin_uuid)

        return sysadmin.is_working()

    def handle_delete(self):

        hr = self._get_hr()

        if self.resource_id is None:
            return

        sysadmin = hr.get_sysadmin(self.resource_id)

        sysadmin.fire()

    def check_delete_complete(self, sysadmin_uuid):
        hr = self._get_hr()

        if self.resource_id is None:
            return True

        sysadmin = hr.get_sysadmin(sysadmin_uuid)

        return sysadmin.is_fired()

    def handle_update(self, json_snippet=None, tmpl_diff=None, prop_diff=None):

        hr = self._get_hr()

        if self.FAVORITE_ANIMAL in prop_diff:

            new_favorite_animal = prop_diff[self.FAVORITE_ANIMAL]

            sysadmin = hr.get_sysadmin(self.resource_id)

            sysadmin.set_favorite_animal(new_favorite_animal)

            return {'favorite_animal': prop_diff[self.FAVORITE_ANIMAL]}

        return None

    def check_update_complete(self, dict):

        hr = self._get_hr()

        sysadmin = hr.get_sysadmin(self.resource_id)

        if dict.get('favorite_animal') == sysadmin.favorite_animal:
            return True
        return False


def resource_mapping():

    mappings = {'OS::Whip::SysAdmin': SysAdmin}
    return mappings
