#def compare_time(ns, cost_function, utility_function, iterations=10):
#    local_times, greedy_times = [], []
#    for j in range(len(ns)):
#        n = ns[j]
#        greedy_time, local_time = 0, 0
#        for i in range(iterations):
#            utility = utility_function(n)
#            cost = cost_function(n)
#            start = time.time()
#            greedydict = toolbox.greedy(cost, utility, n)
#            greedy_time += time.time() - start
#            start = time.time()
#            localdict = toolbox.local(cost, utility, n, toolbox.insert, start=greedydict['ordering'])
#            local_time += time.time() - start
#        local_times += [local_time/iterations]
#        greedy_times += [greedy_time/iterations]
#    plotplot(ns, greedy_times, 'Greedy')
#    plotplot(ns, local_times, 'Local')


#def plotplot(x, y, label):
#    plt.scatter(x, y, label=label)
#    for deg in [2,3]:
#        X = np.linspace(min(x), max(x), num=100)
#        coeffs = np.polyfit(x, y, deg=deg)
#        equation = '+'.join([str(coeffs[i]) + 'x^'+str(deg-i) for i in range(len(coeffs))])
#        Y = np.polyval(coeffs, X)
#        plt.plot(X, Y, label='Least Squares Degree '+str(deg))
#    plt.xlabel('Number of Facilities')
#    plt.ylabel('Time')
#    plt.legend()
#    plt.title('Running Time per Iteration vs Number of Facilities')
#    plt.savefig('graphics/complexity_{}.pdf'.format(label.lower()))
#    plt.clf()

#compare_time(ns=ns, cost_function=modular, utility_function=facilitylocation.genfacility)
