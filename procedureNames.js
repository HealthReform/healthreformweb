var casper = require('casper').create();


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
	
	this.echo(this.fetchText('span.measure-name'));
	this.exit();
});