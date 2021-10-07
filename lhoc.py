#!/usr/bin/env pipenv-shebang

import click
import os
import requests


BASE_URL = os.getenv('LHOC_SERVER')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('level')
def activation(level: int):
    report(post_status('lhoc', level))


@cli.command()
@click.argument('level')
def readcon(level: int):
    report(post_status('readcon', level))


@cli.command()
@click.argument('level')
def seccon(level: str):
    report(post_status('seccon', level))


@cli.group()
def job():
    pass


@job.command()
@click.argument('host')
@click.argument('file')
def asset_linking(host: str, file: str):
    data = {
        'type': 'asset-linking',
        'host': host,
        'file': file,
    }
    post_job(data)


@job.command()
@click.argument('host')
@click.argument('total')
@click.option('--pdf', default=False, type=bool)
def statement_import(host: str, total: int, pdf: bool):
    data = {
        'host': host,
        'total': total,
    }
    if pdf:
        data['type'] = 'fuga-pdf-statements'
    else:
        data['type'] = 'fuga-statements'

    post_job(data)


@job.command()
def stop():
    delete_job()


def post_job(data: dict):
    resp = requests.post(f'{BASE_URL}/job', json=data)
    resp.raise_for_status()


def delete_job():
    resp = requests.delete(f'{BASE_URL}/job')
    resp.raise_for_status()


def post_status(endpoint: str, level) -> dict:
    resp = requests.post(f'{BASE_URL}/{endpoint}', json={'level': level})
    resp.raise_for_status()
    return resp.json()


def report(response: dict):
    print(f"READCON {response['readcon']['level']}")
    print(f"LHOC {response['lhoc']['level']}")
    print(f"SECCON {response['seccon']['level']}")


if __name__ == '__main__':
    cli()
