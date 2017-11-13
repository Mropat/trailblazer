from pathlib import Path

import click
import ruamel.yaml
from tabulate import tabulate

from trailblazer.mip import files


@click.command()
@click.argument('family')
@click.pass_context
def check(context: click.Context, family: str):
    """Delete an analysis log from the database."""
    analysis_obj = context.obj['store'].analyses(family=family).first()
    if analysis_obj is None:
        print(click.style('no analysis found', fg='yellow'))
        context.abort()

    config_raw = ruamel.yaml.safe_load(Path(analysis_obj.config_path).open())
    config_data = files.parse_config(config_raw)

    sampleinfo_raw = ruamel.yaml.safe_load(Path(config_data['sampleinfo_path']).open())
    sampleinfo_data = files.parse_sampleinfo(sampleinfo_raw)

    qcmetrics_raw = ruamel.yaml.safe_load(Path(sampleinfo_data['qcmetrics_path']).open())
    qcmetrics_data = files.parse_qcmetrics(qcmetrics_raw)

    with Path(sampleinfo_data['peddy']['sex_check']).open() as sexcheck_handle:
        peddy_data = files.parse_peddy_sexcheck(sexcheck_handle)

    samples = {'sample': [], 'ped': [], 'chanjo': [], 'peddy': [], 'plink': []}
    for sample_data in sampleinfo_data['samples']:
        samples['sample'].append(sample_data['id'])
        samples['ped'].append(sample_data['sex'])

    for sample_data in qcmetrics_data['samples']:
        samples['chanjo'].append(sample_data['predicted_sex'])
        samples['plink'].append(sample_data['plink_sex'])

    for sample_id in samples['sample']:
        samples['peddy'].append(peddy_data[sample_id]['predicted_sex'])

    print(tabulate(samples, headers='keys', tablefmt='psql'))
