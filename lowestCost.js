var casper = require('casper').create({
    pageSettings: {
        webSecurityEnabled: false
    }
});
var links = [];
var hospitalName = ''
var procedure = ''

function getLinks() {
    var links = document.querySelectorAll('span[class = "unit dollar"]');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href');
    });
}


casper.start('http://www.healthcarereportcard.illinois.gov', function() {

});


casper.then(function() {
    var hospitalName = casper.cli.get(0);
    //this.echo(hospitalName);
	//this.echo(this.getCurrentUrl());
    this.fillSelectors('form#SearchFacilityNameForm', {
         'input[id = "SearchFacilityName"] ' : hospitalName
    }, true);
	

	//this.click('.float-left ui-icon ui-icon-search');
    
});
casper.then(function(){
    // //this.echo(this.getCurrentUrl());
    this.click(" a[href*='/hospitals/' ] ");

});
casper.then(function(){
    // //this.echo(this.getCurrentUrl());
   var procedure = casper.cli.get(1);
    this.echo(this.fetchText(procedure));

});
casper.run(function() {
	//this.echo(this.getCurrentUrl());
   
	this.exit();
});