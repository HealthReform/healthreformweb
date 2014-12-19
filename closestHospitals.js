var casper = require('casper').create();
var links = [];
var hospitalName = ''

function getLinks() {
    var links = document.querySelectorAll('a[href*="/hospitals/"]');
    return Array.prototype.map.call(links, function(e) {
        return e.textContent;
    });
}


casper.start('http://www.healthcarereportcard.illinois.gov', function() {
    //this.echo(this.getCurrentUrl());

});


casper.then(function() {
    var zipCode = casper.cli.get(0);
	//this.echo(this.getCurrentUrl());
    this.fillSelectors('form#SearchesZipcodeForm', {
         'input[id = "SearchZipcode"] ' : zipCode,
         'select[id = "SearchRadius"]'  : '10'
    }, true);

	

	//this.click('.float-left ui-icon ui-icon-search');
    
});
casper.then(function(){

    links = this.evaluate(getLinks);
    //this.echo(this.fetchText( 'a[href*="/hospitals/"]') );

});

casper.run(function() {
	//this.echo(links.length + ' links found:');
    this.echo(' - ' + links.join('\n - ')).exit();
});