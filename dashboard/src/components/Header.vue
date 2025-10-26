<template>
  <header>
    <div class="wrapper">
      <nav>
        <ul>
          <li>
            <RouterLink to="/">Home</RouterLink>
          </li>
          <li>
            <RouterLink to="/trading/live">Trading - live</RouterLink>
          </li>
          <li>
            <RouterLink to="/trading/positions">Trading - positions</RouterLink>
          </li>
          <li>
            <RouterLink to="/trading/history">Trading - history</RouterLink>
          </li>
          <li>
            <RouterLink to="/analytics/performance">Analytics - performance</RouterLink>
          </li>
          <li>
            <RouterLink to="/analytics/ml-insights">Analytics - ML Insights</RouterLink>
          </li>
          <li>
            <RouterLink to="/analytics/sentiment">Analytics - Sentiment</RouterLink>
          </li>
          <li>
            <RouterLink to="/risk">Risk</RouterLink>
          </li>
          <li>
            <RouterLink to="/configuration">Configuration</RouterLink>
          </li>
          <li>
            <RouterLink to="/logs">Logs</RouterLink>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>
<style lang="css" scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

ul {
  list-style-type: none;
  padding: unset;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
