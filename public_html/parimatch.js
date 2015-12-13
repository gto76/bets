var page = require('webpage').create();
var args = require('system').args;
var fs = require('fs');
var address = args[1];
var outfile = args[2];
var user_agent = args[3];
page.settings.userAgent = user_agent;
var page = new WebPage();
page.open(address, function(status){
	browser_check_wait();
});

function browser_check_wait(){
	setTimeout(function(){
		fs.write(outfile, page.content, 'w');
		phantom.exit();
	}, 7000);
}
