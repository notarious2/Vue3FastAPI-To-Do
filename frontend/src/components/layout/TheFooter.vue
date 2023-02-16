<template>
  <footer>
    <p class="footer-text">
      <strong>Bekzod Mirahmedov</strong> &copy; &nbsp;
      {{ new Date().getFullYear() }}
    </p>
  </footer>
</template>

<style scoped>
footer {
  grid-area: footer;
  background-color: bisque;
  /* making FOOTER inside of the grid flexbox */
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: auto;
}
</style>
