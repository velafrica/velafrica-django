from import_export import resources
from import_export.fields import Field

from velafrica.velafrica_sud.models import Container, Report


class ContainerResource(resources.ModelResource):
    """
    Define the Conainter resource for import / export.
    """

    class Meta:
        model = Container
        fields = ('container_no', 'container_n_of_year', 'organisation_from', 'organisation_from__name', 'partner_to',
                  'partner_to__organisation__name', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'logistics',
                  'logistics__name', 'pickup_date', 'shipment_date', 'arrival_port_date', 'arrival_partner_date',
                  'velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth', 'seal_no', 'sgs_certified',
                  'notes')


class ReportResource(resources.ModelResource):
    """
    Define the Conainter resource for import / export.
    """
    economic_bicycles_turnover_USD = Field(readonly=True, attribute='economic_bicycles_turnover_USD',
                                           column_name='economic_bicycles_turnover_USD')
    economic_turnover_total_USD = Field(readonly=True, attribute='economic_turnover_total_USD',
                                        column_name='economic_turnover_total_USD')
    economic_spareparts_turnover_USD = Field(readonly=True, attribute='economic_spareparts_turnover_USD',
                                             column_name='economic_spareparts_turnover_USD')
    economic_services_turnover_USD = Field(readonly=True, attribute='economic_services_turnover_USD',
                                           column_name='economic_services_turnover_USD')
    economic_transport_costs_port_to_organisation_USD = Field(readonly=True,
                                                              attribute='economic_transport_costs_port_to_organisation_USD',
                                                              column_name='economic_transport_costs_port_to_organisation_USD')
    communityproject_reinvest_profit_total_USD = Field(readonly=True,
                                                       attribute='communityproject_reinvest_profit_total_USD',
                                                       column_name='communityproject_reinvest_profit_total_USD')

    class Meta:
        model = Report
