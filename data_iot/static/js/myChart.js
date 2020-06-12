function renderChart(data, labels) {
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'This week',
                data: data,
            }]
        },
    });
}
//const datos=document.getElementById("dato").textContent

// console.log(datos)
// console.log(typeof( datos) ) 
// var json=JSON.parse('{{dato|tojson|safe}}') ;
// console.log(json)
console.log('js')
console.log(json)

$("#renderBtn").click(
    function () {
        data = datos// [20000, 14000, 12000, 15000, 18000, 19000, 22000];
        labels =  ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
        renderChart(data, labels);
    }
);