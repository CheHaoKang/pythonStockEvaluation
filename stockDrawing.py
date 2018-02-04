import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import matplotlib.ticker

if __name__ == "__main__":
    plt.rcParams["figure.figsize"] = [12, 6]    # set figure size to enlarge the plot. Remember to do >>> \includegraphics[width=1.0\textwidth] <<<
    fig, (subplot1, subplot2) = plt.subplots(2, 1,gridspec_kw = {'height_ratios':[5, 1]})#)

    xtickLabels = ['2018-01-16','2018-01-17','2018-01-18','2018-01-19','2018-01-22','2018-01-23','2018-01-24','2018-01-25','2018-01-26','2018-01-29','2018-01-30','2018-01-31','2018-02-01','2018-02-02']
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
    y = np.array([10.3, 11, 10.4, 10.25, 10.15, 10.25, 10.15, 10.2, 10.1, 10.15, 10.1, 10.05, 9.76, 9.79])
    y2 = np.array([10.2583,10.2778,10.2778,10.2806,10.275,10.2778,10.2722,10.2694,10.2556,10.2556,10.2444,10.2361,10.2061,10.1861])
    y3 = np.array([10.253,10.269,10.273,10.275,10.275,10.277,10.275,10.271,10.268,10.265,10.261,10.256,10.2432,10.235])
    yAmount = np.array([8000,23000,1000,0,0,7000,2000,2000,2000,0,0,0,0,0])

    y21 = np.array([44.9819,63.3213,53.3253,41.1058,29.2557,25.0593,18.5581,16.0758,10.7172,8.99663,5.99775,3.9985,2.66567,3.81793])
    y22 = np.array([31.2339,41.9297,45.7282,44.1874,39.2102,34.4932,29.1815,24.8129,20.1143,16.4084,12.9382,9.9583,7.52742,6.29092])

    plt.setp(subplot1, xticks=x, xticklabels=xtickLabels, xlim=[0, 15])#, ylabel='score')
    # plt.xticks(rotation=10)
    for tick in subplot1.get_xticklabels():
        tick.set_rotation(20)
    pL11 = subplot1.plot(x, y, '', label='stockIndex', zorder=10)
    for xCor, yCor in zip(x, y):
        subplot1.text(xCor-0.2, yCor-0.06, str(yCor), weight='bold')
    pL12 = subplot1.plot(x, y2, '', label='stockMA18', zorder=10)
    # for xCor, yCor in zip(x, y2):
    #     subplot1.text(xCor, yCor+0.05, str(yCor), weight='bold')
    pL13 = subplot1.plot(x, y3, '', label='stockMA50', zorder=10)
    # for xCor, yCor in zip(x, y3):
    #     subplot1.text(xCor, yCor-0.05, str(yCor), weight='bold')
    subplot1.plot(0.1,8.99,'ro')
    subplot1.text(0.1, 8.99, str(8.99), weight='bold')

    width = 0.5
    pLBar = subplot1.twinx()
    plt.setp(pLBar, xticks=x, xticklabels=xtickLabels, xlim=[0, 15])#, ylabel='execution time (minutes)')
    pLBar.bar(x, yAmount, width, alpha = 0.2, label='amount', color=['red', 'red', 'green', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red'], zorder=1)
    for xCor, yCor in zip(x-width/2, yAmount):
        pLBar.text(xCor, yCor, str(yCor))

    h1, l1 = subplot1.get_legend_handles_labels()
    lgd = subplot1.legend(h1, l1, loc='upper center', fancybox=True, shadow=False, ncol=5) # http://matplotlib.org/users/legend_guide.html

    # subplot2
    plt.setp(subplot2,xticks=x, xticklabels='')#, ylabel='score')
    pL21 = subplot2.plot(x, y21, '', label='stockK', zorder=10)
    # for xCor, yCor in zip(x, y21):
    #     subplot2.text(xCor-0.08, yCor+1, str("%.2f" % (yCor)), weight='bold')
    pL22 = subplot2.plot(x, y22, '', label='stockD', zorder=10)
    # for xCor, yCor in zip(x, y22):
    #     subplot2.text(xCor-0.08, yCor-10, str("%.2f" % (yCor)), weight='bold')
    subplot2.axhline(y=20, color='g', linestyle='--')
    subplot2.axhline(y=80, color='r', linestyle='-.')

    h2, l2 = subplot2.get_legend_handles_labels()
    lgd2 = subplot2.legend(h2, l2, loc='upper center', fancybox=True, shadow=False, ncol=5) # http://matplotlib.org/users/legend_guide.html

    fig.tight_layout()
    fig.savefig('stockDrawing.png', bbox_inches='tight')