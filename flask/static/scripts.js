
let currentDayIndex = 0;
let currentPageIndex = 0;

function changeDay(indice) {
// Masquer l'élément actuel
    document.getElementById('day' + currentDayIndex).style.display = 'none';
            
    // Mettre à jour l'index du jour
    currentDayIndex = indice;
            
     // Afficher l'élément mis à jour
    document.getElementById('day' + currentDayIndex).style.display = 'block';
}

function changeMenu(indice) {
    // Masquer l'élément actuel
        document.getElementById('page' + currentPageIndex).style.display = 'none';
                
        // Mettre à jour l'index du jour
        currentPageIndex = indice;
                
         // Afficher l'élément mis à jour
        document.getElementById('page' + currentPageIndex).style.display = 'block';
}




function createLineChart(myChart, labels, values) {
    var ctx = myChart.getContext("2d");
    var lineChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "temperature",
                data: values[0],
                fill: false,
                borderColor: "rgb(75, 172, 192)",
                linetension: 0.1
            },
            {
                label: "pression",
                data: values[1],
                fill: false,
                borderColor: "rgb(150, 100, 45)",
                linetension: 0.1
            },
            {
                label: "humidité",
                data: values[2],
                fill: false,
                borderColor: "rgb(15, 200, 115)",
                linetension: 0.1
            },
            {
                label: "pluie",
                data: values[3],
                fill: false,
                borderColor: "rgb(215, 75, 45)",
                linetension: 0.1
            }
        ]
        },
        options: {
            responsive: false
        }
    });
}
