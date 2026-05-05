from workflows.development_graph import DevelopmentGraph


def main():
    graph = DevelopmentGraph()

    task = "Criar CRUD para MonitoringStatus"

    graph.run(task)


if __name__ == "__main__":
    main()