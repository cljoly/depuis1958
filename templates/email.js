
function set_email() {
    // Email obfuscator script 2.1 by Tim Williams, University of Arizona
    // Random encryption key feature by Andrew Moulden, Site Engineering Ltd
    // This code is freeware provided these four comment lines remain intact
    // A wizard to generate this code is at http://www.jottings.com/obfuscator/
    coded = "IQLwNIw@60iK8SVgPa.Tf"
    key = "Q6b7cexkRMwTpa5gBlJ1qFZnsI0UYvhryiNPAu3HVodmLSCGW4jtfD8X9EKzO2"
    shift=coded.length
    link=""
    for (i=0; i<coded.length; i++) {
        if (key.indexOf(coded.charAt(i))==-1) {
        ltr = coded.charAt(i)
        link += (ltr)
        }
        else {
        ltr = (key.indexOf(coded.charAt(i))-shift+key.length) % key.length
        link += (key.charAt(ltr))
        }
    }
    email = document.getElementById("email");
    email.href = "mailto:"+link+"?subject=Des mots doux";
}

document.addEventListener("DOMContentLoaded", function(event) {
    set_email();
});
