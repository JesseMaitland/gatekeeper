from prettytable import PrettyTable
from typing import List
from sty import fg


class AuditResult:

    def __init__(self, results: List) -> None:
        self.results = results

    def print_table(self) -> None:
        table = PrettyTable()

        table.field_names = self.results[0].header

        for field in table.field_names:
            table.align[field] = 'l'

        for result in self.results:
            table.add_row([result.get_display_value(name) for name in result.header])

        print(table)


class BaseAudit:

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def header(self) -> List[str]:
        raise NotImplementedError


class SimpleAudit(BaseAudit):

    def __init__(self, name: str, gatekeeper: bool, redshift: bool, valid: bool):
        super(SimpleAudit, self).__init__(name)
        self._gatekeeper = gatekeeper
        self._redshift = redshift
        self._valid = valid

    @property
    def header(self) -> List[str]:
        return ['name', 'gatekeeper', 'redshift', 'valid']

    @property
    def display_name(self) -> str:
        return f"{fg.green}{self._name}{fg.rs}" if self._valid else f"{fg.red}{self._name}{fg.rs}"

    @property
    def display_gatekeeper(self) -> str:
        return f'{fg.green}yes{fg.rs}' if self._gatekeeper else f'{fg.red}no{fg.rs}'

    @property
    def display_redshift(self) -> str:
        return f'{fg.green}yes{fg.rs}' if self._redshift else f'{fg.red}no{fg.rs}'

    @property
    def display_valid(self) -> str:
        return f'{fg.green}yes{fg.rs}' if self._valid else f'{fg.red}no{fg.rs}'

    def get_display_value(self, name: str) -> str:
        return getattr(self, f"display_{name}")


class Audit:

    @staticmethod
    def perform(gatekeeper_values: List[str], redshift_values: List[str]) -> AuditResult:
        results = []
        gatekeeper_values.sort()
        redshift_values.sort()

        valid_items = list(set(gatekeeper_values).intersection(redshift_values))

        # make list of valid users
        results.extend([SimpleAudit(name, True, True, True) for name in valid_items])
        results.extend([SimpleAudit(name, True, False, False) for name in gatekeeper_values if name not in valid_items])
        results.extend([SimpleAudit(name, False, True, False) for name in redshift_values if name not in valid_items])
        results.sort(key=lambda x: x.name)
        return AuditResult(results=results)




