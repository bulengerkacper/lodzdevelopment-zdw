// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
var keys = { 37: 1, 38: 1, 39: 1, 40: 1 };

function preventDefault(e) {
  e.preventDefault();
}

function preventDefaultForScrollKeys(e) {
  if (keys[e.keyCode]) {
    preventDefault(e);
    return false;
  }
}

// modern Chrome requires { passive: false } when adding event
var supportsPassive = false;
try {
  window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
    get: function () { supportsPassive = true; }
  }));
} catch (e) { }

var wheelOpt = supportsPassive ? { passive: false } : false;
var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';

// call this to Disable
function disableScroll() {
  console.warn('dada');
  window.addEventListener('DOMMouseScroll', preventDefault, false); // older FF
  window.addEventListener(wheelEvent, preventDefault, wheelOpt); // modern desktop
  window.addEventListener('touchmove', preventDefault, wheelOpt); // mobile
  window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

// call this to Enable
function enableScroll() {
  window.removeEventListener('DOMMouseScroll', preventDefault, false);
  window.removeEventListener(wheelEvent, preventDefault, wheelOpt);
  window.removeEventListener('touchmove', preventDefault, wheelOpt);
  window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}

function chooseStreetBtnDisableHandler() {
  disableChoosing($("#chooseStreetInput").val().length == 0);
}

function disableChoosing(flag) {
  // console.log('disableChoosing(flag)', flag, $("#chooseStreetInput").val(), $("#chooseStreetInput").val().length);
  $("#chooseStreetBtn").prop('disabled', flag);
  !flag ? $("#chooseStreetBtn").removeClass('disabled') : $("#chooseStreetBtn").addClass('disabled');
}

var gas, heat;

function initMap() {
  var map = L.map('map').setView([51.593790, 18.949978], 14);
  var lines = [];

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
      '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
  }).addTo(map);

  
  $.ajax({
    type: 'GET',
    contentType: 'application/json;charset=utf-8',
    url: '/heat_network',
    success: function(result) { 
      heat = JSON.parse(result);
      console.log(result);
      JSON.parse(result).forEach(lineCoordinates => {
          console.log(lineCoordinates);
          lineCoordinates.points = lineCoordinates.points.sort();
          let points = lineCoordinates.points.map(p => {
            return new L.LatLng(parseFloat(p.split(' ')[1] * (-1)), parseFloat(p.split(' ')[0]));
          });
          console.log(points);
      
          let newLine = new L.Polyline(points, { color: 'red', weight: 5, smoothFactor: 0, opacity: .3 }).addTo(map);
          newLine.on('click', () => { chooseStreet(lineCoordinates.road) });
          console.log(newLine);
          // newLine
          lines.push(newLine);
        });
    },
    error: function(error) { console.error(error) }
  });

  $.ajax({
    type: 'GET',
    contentType: 'application/json;charset=utf-8',
    url: '/gas_network',
    success: function(result) { 
      gas = JSON.parse(result);
      console.log(result);
      JSON.parse(result).forEach(lineCoordinates => {
          console.log(lineCoordinates);
          lineCoordinates.points = lineCoordinates.points.sort();
          let points = lineCoordinates.points.map(p => {
            return new L.LatLng(parseFloat(p.split(' ')[1] * (-1)), parseFloat(p.split(' ')[0]));
          });
          console.log(points);
      
          let newLine = new L.Polyline(points, { color: 'blue', weight: 5, smoothFactor: 0, opacity: .3 }).addTo(map);
          newLine.on('click', () => { chooseStreet(lineCoordinates.road) });
          console.log(newLine);
          // newLine
          lines.push(newLine);
        });
    },
    error: function(error) { console.error(error) }
  });

  // heat.forEach(lineCoordinates => {
  //   console.log(lineCoordinates);
  //   lineCoordinates.points = lineCoordinates.points.sort();
  //   let points = lineCoordinates.points.map(p => {
  //     return new L.LatLng(parseFloat(p.split(' ')[1] * (-1)), parseFloat(p.split(' ')[0]));
  //   });
  //   console.log(points);

  //   let newLine = new L.Polyline(points, { color: 'red', weight: 5, smoothFactor: 0, opacity: .3 }).addTo(map);
  //   newLine.on('click', () => { chooseStreet(lineCoordinates.road) });
  //   console.log(newLine);
  //   // newLine
  //   lines.push(newLine);
  // });

  // gas.sort();
  // gas.forEach(lineCoordinates => {
  //   console.log(lineCoordinates);
  //   lineCoordinates.points = lineCoordinates.points.sort();
  //   let points = lineCoordinates.points.map(p => {
  //     return new L.LatLng(parseFloat(p.split(' ')[1] * (-1)), parseFloat(p.split(' ')[0]));
  //   });
  //   console.log(points);

  //   let newLine = new L.Polyline(points, { color: 'blue', weight: 5, smoothFactor: 0, opacity: .3 }).addTo(map);
  //   newLine.on('click', () => { chooseStreet(lineCoordinates.road) });
  //   console.log(newLine);
  //   // newLine
  //   lines.push(newLine);
  // });
}

function chooseStreet(street) {
  disableChoosing($("#chooseStreetInput").val(street));
  chooseStreetBtnDisableHandler();

  data.street = street;
  data.isGasAvailable = gas.find(e => e.road == street) != undefined;
  data.isHeatAvailable = heat.find(e => e.road == street) != undefined;
}

function handleEnergySavingLevelRangeChange(range) {
  $(range).next().text(rangeValues.energySavingLevel[$(range).val()]);
  data.buildingEnergySavingLevel = $("#energySavingLevelRange").val().toString();
  checkStepTwoButtonStatus();
}

function handlePeopleRangeChange(range) {
  $(range).next().text($(range).val());
  data.buildingResidents = $("#peopleRange").val().toString();
  checkStepTwoButtonStatus();
}

function handleBuildingSizeChange(input) {
  console.log('handleBuildingSizeChange', input, $(input).val());
  if (isNumeric($(input).val())) {
    console.log('dut git')
    $(input).removeClass('is-invalid');
    data.buildingSize = $(input).val();
  } else {
    $(input).addClass('is-invalid');
    data.buildingSize = null;
  }

  checkStepTwoButtonStatus();
}

function checkStepTwoButtonStatus() {
  console.log('checkStepTwoButtonStatus')
  let disabled = false;
  disabled = disabled || data.buildingSize == null;

  $('#stepTwoContinueBtn').prop('disabled', disabled);
}

function isNumeric(str) {
  console.log('isNumeric', typeof str == "string" ? (!isNaN(str) && !isNaN(parseFloat(str))) : false);
  return typeof str == "string" ? (!isNaN(str) && !isNaN(parseFloat(str))) : false;
}


function nextStep() {
  $('#step-' + meta.step + '-label').removeClass('text-secondary');
  meta.step = meta.step + 1;
  $('#step-' + meta.step + '-label').addClass('text-secondary');

  if (meta.step == 3) {
    getResults();
  } else if (meta.step == 4) {
    getFinancing();
  }

  docSlider.nextPage();
}


function previousStep() {
  $('#step-' + meta.step + '-label').removeClass('text-secondary');
  meta.step = meta.step - 1;
  $('#step-' + meta.step + '-label').addClass('text-secondary');

  if (meta.step == 3) {
    getResults();
  }

  docSlider.prevPage();
}

function getResults () {
  $.ajax({
    type: 'POST',
    contentType: 'application/json',
    url: '/calc',
    dataType: 'json',
    data: JSON.stringify(getFormalisedData()),
    success: function(result) { loadChart(result); },
    error: function(error) { console.error(error) }
  });
}

function getFinancing() {
  
  $.ajax({
    type: 'GET',
    contentType: 'application/json;charset=utf-8',
    url: '/financing',
    success: function(result) { 
      console.log(result);
      JSON.parse(result).forEach(e => {
        printFinancingCard(e);
      })
    },
    error: function(error) { console.error(error) }
  });
}

function printFinancingCard(cardData) {
  $('<div class="col-6 card-container"> <label class="card p-3"> <p> <p class="w-25 h-25 text-center mx-auto d-flex"> <img class="h-100 my-auto mx-auto" src="../static/images/cash.svg" /> </p> <h5 class="text-center">' + cardData.name +  '</h5> <span class="text-justify">' + cardData.description + '</span></p> <a href="' + cardData.info_url + '" class="btn btn-primary rounded float-left">Dowiedz się więcej</a> <a href="' + cardData.application_url + '" class="btn btn-secondary rounded float-right mt-2">Złóż wniosek</a> </label> </div>').appendTo('#financingContainer');
}

function getFormalisedData() {
  let result = {
    "location": {
        "adress": data.street,
        "area": data.buildingSize,
        "type": data.buildingEnergySavingLevel,
        "users": data.buildingResidents
    },
    "mediums": ["electricity", "gas_tank", "biomass"],
    "period": "1"
  };

  if (data.isGasAvailable) {
    result.mediums.push("gas");
  }
  
  if (data.isHeatAvailable) {
    result.mediums.push("network_heat");
  }

  return result;
}

function loadChart(data) {
  console.log(data);
  chartData = data;

  google.charts.load('current', {packages: ['corechart', 'table']});
  google.charts.setOnLoadCallback(drawChart);
  google.charts.setOnLoadCallback(drawTable);
}

function drawChart() {
  let headers = ['Lata'];
  if (data.isGasAvailable) { headers.push('Gaz z sieci'); }
  if (data.isHeatAvailable) { headers.push('Ciepło miejskie'); }
  headers = headers.concat(['Gaz', 'Elektro', 'Biomasa', 'Węgiel'])
  let d = google.visualization.arrayToDataTable([
    headers,
    getDataForYear(0),
    getDataForYear(1),
    getDataForYear(2),
    getDataForYear(5),
    getDataForYear(10),
    getDataForYear(11),
    getDataForYear(12),
    getDataForYear(13),
    getDataForYear(14),
    getDataForYear(15),
    getDataForYear(16),
    getDataForYear(17),
    getDataForYear(18),
    getDataForYear(19),
    getDataForYear(20)
  ]);

  let options = {
    title: 'Koszt instalacji w przeciagu 20 lat',
    curveType: 'function',
    legend: { position: 'right' },
    vAxis: {title: "Koszt instalacji po upływie x lat"},
    hAxis: {title: "Lata"},
  };
  
  let chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

  chart.draw(d, options);
}

function drawTable() {
  let d = new google.visualization.DataTable();
  d.addColumn('string', 'Źródło');
  d.addColumn('string', 'instalacja [zł]');
  d.addColumn('string', 'koszt po roku [zł]');
  d.addColumn('string', '5 lat [zł]');
  d.addColumn('string', '10 lat [zł]');
  d.addColumn('string', '20 lat [zł]');
  if (data.isGasAvailable) {
    d.addRows([
      ['Gaz z sieci', chartData['gas'] ? chartData['gas'][0][0].total.toFixed(2).toString() : '0.00', chartData['gas'] ? chartData['gas'][0][1].total.toFixed(2).toString() : '0.00', chartData['gas'] ? chartData['gas'][0][5].total.toFixed(2).toString() : '0.00', chartData['gas'] ? chartData['gas'][0][10].total.toFixed(2).toString() : '0.00', chartData['gas'] ? chartData['gas'][0][20].total.toFixed(2).toString() :'0.00']
    ]);
  }
  if (data.isHeatAvailable) {
    d.addRows([
      ['Ciepło miejskie', chartData['network_heat'] ? chartData['network_heat'][0][0].total.toFixed(2).toString() : '0.00', chartData['network_heat'] ? chartData['network_heat'][0][1].total.toFixed(2).toString() : '0.00', chartData['network_heat'] ? chartData['network_heat'][0][5].total.toFixed(2).toString() : '0.00', chartData['network_heat'] ? chartData['network_heat'][0][10].total.toFixed(2).toString() : '0.00', chartData['network_heat'] ? chartData['network_heat'][0][20].total.toFixed(2).toString() :'0.00']
    ]);
  }
  d.addRows([
    ['Gaz', chartData['gas_tank'] ? chartData['gas_tank'][0][0].total.toFixed(2).toString() : '0.00', chartData['gas_tank'] ? chartData['gas_tank'][0][1].total.toFixed(2).toString() : '0.00', chartData['gas_tank'] ? chartData['gas_tank'][0][5].total.toFixed(2).toString() : '0.00', chartData['gas_tank'] ? chartData['gas_tank'][0][10].total.toFixed(2).toString() : '0.00', chartData['gas_tank'] ? chartData['gas_tank'][0][20].total.toFixed(2).toString() :'0.00'],
    ['Elektryczność', chartData['electricity'] ? chartData['electricity'][0][0].total.toFixed(2).toString() : '0.00', chartData['electricity'] ? chartData['electricity'][0][1].total.toFixed(2).toString() : '0.00', chartData['electricity'] ? chartData['electricity'][0][5].total.toFixed(2).toString() : '0.00', chartData['electricity'] ? chartData['electricity'][0][10].total.toFixed(2).toString() : '0.00', chartData['electricity'] ? chartData['electricity'][0][20].total.toFixed(2).toString() :'0.00'],
    ['Biomasa', chartData['biomass'] ? chartData['biomass'][0][0].total.toFixed(2).toString() : '0.00', chartData['biomass'] ? chartData['biomass'][0][1].total.toFixed(2).toString() : '0.00', chartData['biomass'] ? chartData['biomass'][0][5].total.toFixed(2).toString() : '0.00', chartData['biomass'] ? chartData['biomass'][0][10].total.toFixed(2).toString() : '0.00', chartData['biomass'] ? chartData['biomass'][0][20].total.toFixed(2).toString() :'0.00'],
    ['Węgiel', '0.00', chartData['coal'] ? chartData['coal'][0][0].total.toFixed(2).toString() : '0.00', chartData['coal'] ? (chartData['coal'][0][0].total * 5).toFixed(2).toString() : '0.00', chartData['coal'] ? (chartData['coal'][0][0].total * 10).toFixed(2).toString() : '0.00', chartData['coal'] ? (chartData['coal'][0][0].total * 20).toFixed(2).toString() :'0.00']
  ]);
  

  let t = new google.visualization.Table(document.getElementById('data_table'));
  t.draw(d, {showRowNumber: false, width: '100%', height: '100%'});
}

function getDataForYear(yearsPassed) {
  let result = [yearsPassed];
  if (data.isGasAvailable) { result.push(chartData['gas'] ? chartData['gas'][0][yearsPassed].total : 0.0); }
  if (data.isHeatAvailable) { result.push(chartData['network_heat'] ? chartData['network_heat'][0][yearsPassed].total : 0.0); }
  result = result.concat([
    chartData['gas_tank'] ? chartData['gas_tank'][0][yearsPassed].total : 0.0,
    chartData['electricity'] ? chartData['electricity'][0][yearsPassed].total : 0.0,
    chartData['biomass'] ? chartData['biomass'][0][yearsPassed].total : 0.0,
    chartData['coal'] ? chartData['coal'][0][0].total * yearsPassed : 0.0
  ]);

  return result;
}

var chartData;

var data = {
  street: '',
  isGasAvailable: false,
  isHeatAvailable: false,
  buildingSize: null,
  buildingEnergySavingLevel: '1',
  buildingResidents: '4'
}

var meta = {
  step: 1,
}

var rangeValues = {
  'energySavingLevel': {
    1: 'bardzo niski',
    2: 'niski',
    3: 'średni',
    4: 'wysoki',
    5: 'bardzo wysoki'
  }
}