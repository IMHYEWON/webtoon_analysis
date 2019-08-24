// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


var ctx = document.getElementById('myLineChart');
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["38화", "39화", "40화", "41화", "42화"],
        datasets: [{
            label: '별점 변화율',
            data: [9.55, 9.35, 9.27, 9.72, 9.76],
            fill : false,
            borderColor:  "rgba(255, 206, 86, 1)",
            pointRadius: 3,
            pointBackgroundColor: "rgba(255, 206, 86, 1)",
            pointBorderColor: "rgba(255, 206, 86, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(255, 206, 86, 1)",
            pointHoverBorderColor: "rgba(255, 206, 86, 1)",
            lineTension : 0.1 }]
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          gridLines: {
            display: false,
            drawBorder: false
          },
        }],
        yAxes: [{
          ticks: {
            maxTicksLimit: 5,
            padding: 10,
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
          }
        }],
      },
      legend: {
        display: false
      },
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        borderColor: '#dddfeb',
        borderWidth: 2,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        intersect: false,
        mode: 'index',
        caretPadding: 10,
      }
    }
});
