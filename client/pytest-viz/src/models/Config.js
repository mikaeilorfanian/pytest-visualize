export default {
  getAuto(){
    const auto = localStorage.getItem('auto');
    if (auto){
      if (auto === 'false'){
        return null;
      }
      else{
        return 'true';
      }
    }
    else{
      return null;
    }
  },
  saveConfig(vueComponent){
    localStorage.setItem('auto', vueComponent.auto);
  }
}
