#!/usr/bin/env pipenv-shebang

import click
import requests


BASE_URL = 'http://10.0.0.25:5000'


@click.group()
def cli():
    pass


@cli.command()
@click.argument('level')
def activation(level: int):
    report(post('lhoc', level))


@cli.command()
@click.argument('level')
def readcon(level: int):
    report(post('readcon', level))


@cli.command()
@click.argument('level')
def seccon(level: str):
    report(post('seccon', level))


def post(endpoint: str, level) -> dict:
    resp = requests.post(f'{BASE_URL}/{endpoint}', json={'level': level})
    resp.raise_for_status()
    return resp.json()


def report(response: dict):
    print(f"READCON {response['readcon']['level']}")
    print(f"LHOC {response['lhoc']['level']}")
    print(f"SECCON {response['seccon']['level']}")


if __name__ == '__main__':
    cli()
