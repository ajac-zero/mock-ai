<script>
  import { onMount } from "svelte";
  import { API_URL } from "../state.svelte";

  let { number, select_choice = "text", input = "", output = "" } = $props();

  if (typeof output === "object") {
    output = JSON.stringify(output);
  }

  let is_function = $state(false);

  function change_type() {
    is_function = select_choice === "function";
  }

  async function update_responses() {
    let body = {
      number: number,
      new_response: {
        type: select_choice,
        input: input,
        output: output,
      },
    };
    let res = await fetch(API_URL + "/responses/update", {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });
    await res.json();

    window.location.reload();
  }

  async function delete_responses() {
    let url = API_URL + "/responses/delete?number=" + String(number);
    await fetch(url, { method: "DELETE" });

    window.location.reload();
  }

  onMount(change_type);
</script>

<div
  class="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden mb-5"
>
  <div class="px-6 py-4">
    <!-- Title -->
    <div class="font-bold text-xl text-gray-800 mb-4">Response {number}</div>

    <!-- Type Selector -->
    <div class="mb-4">
      <label for="select-type" class="block text-gray-700 font-medium mb-2"
        >Type</label
      >
      <select
        name="type"
        id="select-type"
        class="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        bind:value={select_choice}
        onchange={change_type}
      >
        <option value="text">Text</option>
        <option value="function">Function</option>
      </select>
    </div>

    <!-- Input Field -->
    <div class="mb-4">
      <label for="input" class="block text-gray-700 font-medium mb-2"
        >Input</label
      >
      <textarea
        id="input"
        class="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        bind:value={input}
        rows="3"
        placeholder="Enter input here"
      ></textarea>
    </div>

    <!-- Output Field -->
    <div class="mb-4">
      <label for="output" class="block text-gray-700 font-medium mb-2"
        >Output</label
      >
      <textarea
        id="output"
        class="w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        bind:value={output}
        rows="3"
        placeholder="Enter output here"
      ></textarea>
    </div>

    <!-- Button Container -->
    <div class="flex space-x-4 justify-end">
      <!-- Update Button -->
      <div>
        <button
          class="bg-blue-500 text-white px-4 py-2 rounded-md shadow hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
          onclick={update_responses}
        >
          Update
        </button>
      </div>

      <!-- Delete Button -->
      <div>
        <button
          class="bg-red-500 text-white px-4 py-2 rounded-md shadow hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2"
          onclick={delete_responses}
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</div>
