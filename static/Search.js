//https://api.spotify.com/v1/search?query=&offset=0&limit=20&type=artist
function searchsptfy(query, lim, offset) {
    var seurl = "https://api.spotify.com/v1/search?query=" + query + "&offset=" + offset + "&limit=" + lim + "&type=track";
    $.ajax({
        url: seurl,
        cache: false
    }).done(function (res) {
        return (res); }
           );
}
function cleanUp(res) {
    var retval,c = 0;
    obj = JSON && JSON.parse(res) || $.parseJSON(res);
    for(var track in obj["tracks"]["items"]){
        retval[c]["image"]=track["album"]["images"][1]["url"]
        retval[c]["trname"]=track["Name"];
        retval[c]["alname"]=track["album"]["name"];
        retval[c]["preview"]=track["preview_url"];
        var artlist;
        for(var artist in track["artists"]){
            artlist += artist+", "
        }
        retval[c]["artists"]= artlist.slice(0, -2);
    }
    return retval;
}
function tableString(clean){
    for(var track in clean){
        alArt = "<td><img src="+track["image"]+"/></td>";
        trackname = "<td>"+track["trname"]+"</td>";
        
        
        
    }
}
/*
<div class="table-wrapper">
    <table class="alt">
        <thead>
            <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Item One</td>
                <td>Ante turpis integer aliquet porttitor.</td>
                <td>29.99</td>
            </tr>
            <tr>
                <td>Item Two</td>
                <td>Vis ac commodo adipiscing arcu aliquet.</td>
                <td>19.99</td>
            </tr>
            <tr>
                <td>Item Three</td>
                <td> Morbi faucibus arcu accumsan lorem.</td>
                <td>29.99</td>
            </tr>
            <tr>
                <td>Item Four</td>
                <td>Vitae integer tempus condimentum.</td>
                <td>19.99</td>
            </tr>
            <tr>
                <td>Item Five</td>
                <td>Ante turpis integer aliquet porttitor.</td>
                <td>29.99</td>
            </tr>
        </tbody>
        <tfoot>
            <tr>
                <td colspan="2"></td>
                <td>100.00</td>
            </tr>
        </tfoot>
    </table>
</div>
    */