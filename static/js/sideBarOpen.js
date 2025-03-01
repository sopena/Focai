var active = false

function sidebar_btn_click()
{   console.log(active)
    var bar = document.querySelector('.sidebar');
    var symbol = document.querySelector(".symbol");
    var button = document.querySelector(".sidebar_btn")
    if(active)
    {   
        button.style.transition = ".5s"
        button.style.backgroundColor = "#FF6F6F"
        bar.style.width = "0%";
        symbol.style.marginLeft = "10rem"
        active = false;
    }
    else if(!active)
    {
        button.style.transition = ".5s"
        button.style.backgroundColor = "transparent"
        bar.style.width = "20%";
        symbol.style.marginLeft = "4rem"
        active = true;
    }
    return
}