var active = false

function sidebar_btn_click()
{   console.log(active)
    var bar = document.querySelector('.sidebar');
    var symbol = document.querySelector(".symbol");
    if(active)
    {
        bar.style.width = "0%";
        symbol.style.marginLeft = "10%"
        active = false;
    }
    else if(!active)
    {
        bar.style.width = "20%";
        symbol.style.marginLeft = "2%"
        active = true;
    }
    return
}