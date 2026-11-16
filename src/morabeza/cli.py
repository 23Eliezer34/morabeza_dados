"""Linha de comandos do projeto Morabeza (Sessão 3).

Uso:  python -m morabeza.cli --ilha Sal
"""
import argparse
import logging
import sys

from morabeza.apoio import faturacao_por_ilha, ler_vendas
from morabeza.config import carregar_config

logger = logging.getLogger(__name__)


def criar_parser() -> argparse.ArgumentParser:
    # TODO 5: cria um argparse.ArgumentParser com dois argumentos opcionais:
    #         --config (por defeito "config.yaml") e --ilha (sem valor por defeito).
    parser = argparse.ArgumentParser(description="Linha de comandos do projeto Morabeza.")
    parser.add_argument("--config", default="config.yaml", help="Caminho para o ficheiro de configuração")
    parser.add_argument("--ilha", default=None, help="Nome da ilha para filtrar a faturação") 
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = criar_parser().parse_args(argv)

    # TODO 6: carrega a configuração (args.config) e lê as vendas do ficheiro indicado nela.
    # TODO 7: regista no log: logger.info("Li %d vendas de %s", ...). Não uses print para isto.
    # TODO 8: calcula a faturação por ilha. Sem --ilha, imprime "Faturação total: <valor> <moeda>".
    #         Com --ilha, imprime "Faturação em <ilha>: <valor> <moeda>".
    #         Se a ilha não existir, logger.error(...) e devolve 1. No fim, devolve 0.
    config = carregar_config(args.config) 
    ficheiro_vendas = config["ficheiro_vendas"] 
    moeda = config["moeda"] 
    vendas = ler_vendas(ficheiro_vendas)

    logger.info("Li %d vendas de %s", len(vendas), ficheiro_vendas)

    faturacao = faturacao_por_ilha(vendas) 
    if args.ilha: 
        if args.ilha not in faturacao: 
            logger.error("A ilha '%s' não foi encontrada nos registos de vendas.", args.ilha) 
            return 1 
        print(f"Faturação em {args.ilha}: {faturacao[args.ilha]} {moeda}") 
    else: 
        total = sum(faturacao.values()) 
        print(f"Faturação total: {total} {moeda}") 
    return 0
    
if __name__ == "__main__":
    sys.exit(main())
