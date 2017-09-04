var ws = new WebSocket("ws://localhost:8878/ws");

ws.onmessage = function(e) {
    getdata = eval('(' + e.data + ')');
    console.log(getdata);
};


var DT = function() {
	ws.send("initv");
    // ws.send("q_tree");
}
setTimeout('DT()', 100);

$("#q_g").bind("click",function(){
  ws.send("q_tree");
});