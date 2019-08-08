import matplotlib.pyplot as graph

from codesamples import hodgkin_huxley_squid_axon_model_1952 as hh


def main():
    step_size = 0.001

    rates = hh.createRateVector()
    states = hh.createStateVector()
    variables = hh.createVariableVector()

    hh.initializeConstants(states, variables)
    hh.computeComputedConstants(variables)

    results = [ [] for _ in range(len(states)) ]
    x = []
    t = 0.0
    end = 65.35
    while t < end:
        hh.computeRates(t, states, rates, variables)
        delta = list(map(lambda x: x * step_size, rates))
        states = [sum(x) for x in zip(states, delta)]

        x.append(t)
        for index, value in enumerate(states):
            results[index].append(value)

        t += step_size

    graph.xlabel("Time (msecs)")
    graph.ylabel("Y-axis")
    graph.title("A test graph")
    for index, result in enumerate(results):
        graph.plot(x, result, label='id {0}'.format(index))
    graph.legend()
    graph.show()


if __name__ == "__main__":
    main()
