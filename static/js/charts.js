 window.onload = function () {
var chart = c3.generate({
         bindto: '#chart',
         data: {
          url: 'http://localhost:5010/calls/months',
		  mimeType: 'json',
          keys: {
            x: '_id',
            value: ['number_of_calls'],
          }
        },
        axis: {
          x: {
            type: 'categorized'
          },
	
        },
		size: {
      height: 300,
	  width: 1000
        }
      });
//////////////////////////////////////////////////////
 $.getJSON("http://localhost:5010/agent/calls", function(jsonData) {
var data = {};
var sites = [];
jsonData.forEach(function(e) {
    sites.push(e._id);
    data[e._id] = e.number_of_calls;
})    

var charttt = c3.generate({
bindto: '#charttt',
    data: {
        json: [ data ],
        keys: {
            value: sites,
        },
        type:'pie'
    },
});
 });

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var chart = c3.generate({
         bindto: '#chartt',
         data: {
          url: 'http://localhost:5010/agent/months',
		  mimeType: 'json',
          keys: {
            x: 'month',
            value: ['FATMA MNEKBI','KARIM KASBAOUI','LEILA SMINE MEHRI','OLFA MAHJOUB BOUOUN','SAMI BEN HASSEN','SAMI BEN JILANI','SONIA ELLOUZE',''],
          }
        },
        axis: {
          x: {
            type: 'categorized'
          },
	
        },
		size: {
      height: 300,
	  width: 1200
        }
      });

//////////////////////////////////////////////////////////////////////
 $.getJSON("http://localhost:5010/calls/months", function(jd) {
 var s=0;
for(var i = 0 ; i < jd.length ; i++){
s=s+parseFloat(jd[i].number_of_calls);
}
var ch=s.toString();
$('#stage').html('<p>' + ch + '</p>');	  
 });
 ///////////////////////////////////////////
 $.getJSON("http://localhost:5010/agent/calls", function(jd) {

var ch=jd.length.toString();
$('#stagee').html('<p>' + ch + '</p>');

	  
 });
 }
 