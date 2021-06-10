document.getElementById("domain").innerHTML = "shubhamkumar"
var url = '{ data["url"] }';
var result = '{{ data["prediction"] }}';
var domain = '{{ data["domain"] }}';
var ip = '{{ data["ipadd"] }}';
var cred_date = '{{ data["creation_date"] }}';
var exp_date = '{{ data["expiration_date"] }}';
         

document.getElementById("url").innerHTML = url

if(result == 0){
    document.getElementById("result").innerHTML = 'This URL is Suspicious';
}
else if(result == 1){
    document.getElementById("result").innerHTML = 'This URL is legitimate';
}
else if(result == 2){
    document.getElementById("result").innerHTML = "This URL doesn't exist";
}        