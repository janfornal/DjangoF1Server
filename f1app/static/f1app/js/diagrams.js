function plot_diagrams(results_visual) {
    var count = results_visual.length;
    for(var i = 0; i < count; i++) {
        var ctx = document.getElementsByClassName('canvas ' + results_visual[i].id)
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(results_visual[i].results),
                datasets: [{
                    label: '#',
                    data: Object.values(results_visual[i].results),
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}