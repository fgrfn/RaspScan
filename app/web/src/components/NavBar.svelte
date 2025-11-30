<script>
  export let brand = 'RaspScan';
  export let links = [];
  export let currentLang = 'en';
  export let onLanguageChange = () => {};
</script>

<header class="topbar">
  <div class="brand">
    <div class="logo">📠</div>
    <div>
      <div class="brand-name">{brand}</div>
      <div class="brand-sub">Scan Hub</div>
    </div>
  </div>
  <nav class="links">
    {#each links as link}
      <a class="link" href={link.href}>{link.label}</a>
    {/each}
    <select 
      bind:value={currentLang} 
      on:change={(e) => onLanguageChange(e.target.value)}
      style="margin-left: 1rem; padding: 0.25rem 0.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: 4px; color: var(--text); font-size: 0.875rem; cursor: pointer;"
    >
      <option value="en">🇬🇧 EN</option>
      <option value="de">🇩🇪 DE</option>
    </select>
  </nav>
</header>
