<template>
  <div id="loading"></div>
</template>

<style scoped>
#loading {
  display: inline-block;
  width: 35px;
  height: 35px;
  position: relative;
  margin-left: auto;
  margin-right: auto;
  margin-top: 30px;
  left: 0;
  right: 0;
  bottom: 1px;
  padding: 0px;
  border: 3px solid rgba(139, 155, 48, 0.3);
  border-radius: 50%;
  border-top-color: rgb(192, 138, 46);
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}
@-webkit-keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}
</style>
