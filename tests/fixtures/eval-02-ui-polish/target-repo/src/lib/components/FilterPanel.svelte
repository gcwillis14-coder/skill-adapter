<script lang="ts">
  interface Props {
    selectedLayer: string;
    onSelect: (layer: string) => void;
  }

  let { selectedLayer, onSelect }: Props = $props();
  let expanded = $state(false);
</script>

<div class="panel">
  <div class="toggle" onclick={() => (expanded = !expanded)}>
    Layer: {selectedLayer}
  </div>
  {#if expanded}
    <button type="button" onclick={() => onSelect('parcels')}>Parcels</button>
  {/if}
</div>

<style>
  .panel {
    background: #ffffff;
    color: #9aa0a6;
    padding: 0.75rem;
  }
  .toggle {
    cursor: pointer;
  }
</style>
