<template>
  <div class="post-it-note">
    <slot></slot>
  </div>
</template>

<style scoped>
.post-it-note {
  margin: 20px 0px 0px 10px;
  padding: 1em;
  background: #ffffd4;
  position: relative;
  min-height: 10em;
  margin-bottom: 30px;
  box-shadow: rgba(17, 17, 26, 0.05) 0px 4px 16px,
    rgba(17, 17, 26, 0.05) 0px 8px 32px;
}
.post-it-note:after {
  content: "";
  position: absolute;
  bottom: -2em;
  left: 0;
  right: 2em;
  border-width: 1em;
  border-style: solid;
  border-color: #ffffd4;
}
.post-it-note:before {
  content: "";
  position: absolute;
  bottom: -2em;
  right: 0;
  border-width: 2em 2em 0 0;
  border-style: solid;
  border-color: #dcdc46 transparent;
}

@media (max-width: 768px) {
  .post-it-note {
    margin-right: 10px;
  }
}
</style>
