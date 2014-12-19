var casper = require('casper').create();
var links = [];


function getLinks() {
    var links = document.querySelectorAll('h3.r a');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href');
    });
}


casper.start('http://www.healthcarereportcard.illinois.gov', function() {

    var hospitalName = casper.cli.get(0);
    this.fillSelectors('form#SearchFacilityNameForm', {
    	 'input[id = "SearchFacilityName"] ' : hospitalName
    }, true);
    
    //this.echo(this.getCurrentUrl());
    //this.echo(casper.cli.get(0));
   
    
});


casper.then(function() {
	//this.echo(this.getCurrentUrl());
	this.click(" a[href*='/hospitals/'] ");

	//this.click('.float-left ui-icon ui-icon-search');
    
});

casper.run(function() {
	//this.echo(this.getCurrentUrl());
	//this.echo(this.fetchText('td.numberofpatients.measure-value'));
	this.echo(this.fetchText('td.mediancharges.measure-value'));
	this.exit();
});