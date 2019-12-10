export default {
    getAuto(){
        const auto = localStorage.getItem('auto');
        if (auto){
            console.log('auto config already set');
            if (auto === 'false'){
                return null;
            }
            else{
                return 'true';
            }
        }
        else{
            console.log('auto config NOT set');
            return null;
        }
    },
  }
