
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

token = getCookie('csrftoken')
 

function get_fp(){


const fpPromise = import('https://openfpcdn.io/fingerprintjs/v3')
.then(FingerprintJS => FingerprintJS.load())


fpPromise
    .then(fp => fp.get())
    .then(result => {
    
        const components = result.components
        const canvas_geomentry=components.canvas.value.geometry
        const canvas_text=components.canvas.value.text
        const colorDepth = components.colorDepth.value
        const fonts=components.fonts.value
        const plugins = components.plugins.value
        const resolution= components.screenResolution.value
        const hardwareConcurrency = components.hardwareConcurrency.value               
        const math = components.math.value
        const platform =components.platform.value
        const audio =components.audio.value
        const max_touch =components.touchSupport.value.maxTouchPoints
        const index_db =components.indexedDB.value
        const localStorage =components.localStorage.value
        const fontPreferences=components.fontPreferences.value
        const gamut = components.colorGamut.value

        let plugins_len = plugins.length
        let plugins_array = []
        
        for(let i=0;i<plugins_len;i++){
            plugins_array[i]=plugins[i].name.toString()
        }
       
    
        
    
        data={
            'fonts': fonts.toString(),
                'canvas_geometry': canvas_geomentry,
                'canvas_text':canvas_text,
                'colorDepth': colorDepth,
                'plugins': plugins_array.toString(),
                'resolution':resolution.toString(),
                'hardwareConcurrency': hardwareConcurrency,
                'math': math,
                'platform': platform,
                'audio': audio,
                'max_touch':max_touch,
                'index_db': index_db,
                'localStorage': localStorage,
                'fontPreferences': fontPreferences,
                'gamut': gamut
            }
        
        $.ajax({
        headers: { "X-CSRFToken": token },
        type:"POST",
        url: Request.this,
       // data: data,
      
        data:data,
        dataType:"text",     
        cache: false,
        
         
    });
 
})

}
document.getElementById("#reg_button").onclick = get_fp()