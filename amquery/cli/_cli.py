import click
import os
from bunch import Bunch
from typing import List
import configparser
import amquery.utils.iof as iof
from amquery.utils.config import get_default_config
from amquery.utils.multiprocess import Pool
from amquery.core.distance import distances, DEFAULT_DISTANCE
from amquery.core import Index


pass_config = click.make_pass_decorator(configparser.ConfigParser(), ensure=True)


def _index_check(config):
    message = "There is no index created. Run 'amq init' first"
    assert "current_index" in config, message
    assert iof.exists(config.index_path), message


def _build_check(config):
    if config.built.lower() != "true":
        raise ValueError("First you have to build the index. Run 'amq build'")


@click.group()
@click.option('--force', '-f', is_flag=True, help='Force overwrite output directory')
@click.option('--quiet', '-q', is_flag=True, help='Be quiet')
@click.option('--jobs', '-j', type=int, default=1, help='Number of jobs to start in parallel')
def cli(force: bool, quiet: bool, jobs: int):
    #config = Config.load()
    #config.temp.force = force
    #config.temp.quiet = quiet
    #config.temp.jobs = jobs

    Pool.instance(jobs=jobs)


@cli.command()
@click.argument("name", type=str, required=False)
@click.option("--method", type=click.Choice(distances.keys()), default=DEFAULT_DISTANCE)
@click.option("--rep_tree", type=click.Path())
@click.option("--rep_set", type=click.Path())
@click.option("--kmer_size", "-k", type=int, default=15)
def init(name, method, rep_tree, rep_set, kmer_size):
    index_dir = os.path.join(os.getcwd(), name, '.amq') if name else os.path.join(os.getcwd(), '.amq')
    iof.make_sure_exists(index_dir)
    index_path = os.path.join(index_dir, 'config')

    config = get_default_config()
    config.set('config', 'path', index_path)
    config.set('distance', 'method', method)
    if rep_tree:
        config.set('distance', 'rep_tree', rep_tree)
    if rep_set:
        config.set('distance', 'rep_set', rep_set)
    if kmer_size:
        config.set('distance', 'kmer_size', str(kmer_size))

    with open(config.get('config', 'path'), 'w') as f:
        config.write(f)


@cli.command()
@click.argument('input_files', type=click.Path(exists=True), nargs=-1,
                required=True)
def build(input_files: List[str]):
    index = Index.build(input_files)
    index.save()


@cli.command()
@click.option('--kmer_size', '-k', type=int, help='K-mer size', default=15)
@click.option('--distance', '-d', type=click.Choice(distances.keys()),
              default='jsd', help='A distance metric')
@pass_config
def refine(config, kmer_size: int, distance: str):
    _index_check(config)

    config.dist = Bunch()
    config.dist.func = distance
    config.dist.kmer_size = kmer_size

    index = Index.load(config)
    index.refine()
    index.save()

    config.built = "true"
    config.save()


@cli.command()
@click.argument('input_files', type=click.Path(exists=True), nargs=-1,
                required=True)
@pass_config
def add(config, input_files: List[str]):
    _index_check(config)

    index = Index.load(config)
    index.add(input_files)
    index.save()


@cli.command()
@pass_config
def stats(config):
    _index_check(config)
    _build_check(config)

    index = Index.load(config)
    indexed = len(index.sample_map)

    click.secho("Current index: ", bold=True, nl=False)
    click.secho(str(config.current_index))
    click.secho("Indexed: ", bold=True, nl=False)
    click.secho("%s samples" % indexed)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True),
                required=True)
@click.option('-k', type=int, required=True,
              help='Count of nearest neighbors')
@pass_config
def find(config, input_file: str, k: int):
    _index_check(config)
    _build_check(config)

    index = Index.load(config)
    values, points = index.find(input_file, k)
    click.secho("%s nearest neighbors:" % k, bold=True)
    click.secho('\t'.join(x for x in ['Hash', 'Sample', 'Similarity']), bold=True)

    for value, sample in zip(values, points):
        click.secho("%s\t" % sample.name[:7], fg='blue', nl=False)
        click.echo(sample.original_name if len(sample.original_name) <= 8 else sample.original_name[:5] + "..", nl=False)
        click.echo("\t%f\t" % value)
