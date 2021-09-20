


function filter_tel(tel, data){}
var lst = []
for(telcode of  data ){
    if( telcode['tel'].startswith(tel)){
        lst.append(telcode)
    }

return lst
}