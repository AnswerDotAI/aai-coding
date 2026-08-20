(() => {
  const panelId = "claude-chat-exporter";
  const pageLimit = 1000;
  const projectConcurrency = 3;
  const chatConcurrency = 2;
  document.getElementById(panelId)?.remove();

  const api = async path => {
    for (let attempt = 0; attempt < 4; attempt++) {
      const response = await fetch(path, {
        credentials: "include",
        headers: { Accept: "application/json" },
      });
      if (response.ok) return response.json();
      if (response.status !== 429 || attempt === 3) {
        const error = new Error(`${response.status} ${response.statusText}: ${path}`);
        error.status = response.status;
        error.path = path;
        throw error;
      }
      const wait = Number(response.headers.get("retry-after") || attempt + 1) * 1000;
      await new Promise(resolve => setTimeout(resolve, wait));
    }
  };

  const rows = value => {
    if (Array.isArray(value)) return value;
    for (const key of ["data", "results", "items"]) {
      if (Array.isArray(value?.[key])) return value[key];
    }
    return [];
  };

  const json = value => JSON.stringify(value, null, 2) + "\n";
  const now = () => new Date().toISOString();
  const currentChatUuid = location.pathname.match(/\/chat\/([0-9a-f-]{36})/i)?.[1];
  const currentProjectUuid = location.pathname.match(/\/project\/([0-9a-f-]{36})/i)?.[1];
  const linkedUuid = selector => document.querySelector(selector)?.getAttribute("href")?.match(/([0-9a-f-]{36})/i)?.[1];
  const visibleChatUuid = currentChatUuid || linkedUuid('a[href^="/chat/"]');
  const visibleProjectUuid = currentProjectUuid || linkedUuid('a[href*="/project/"]');

  const pool = async (items, limit, fn) => {
    const output = new Array(items.length);
    let next = 0;
    const worker = async () => {
      while (next < items.length) {
        const index = next++;
        output[index] = await fn(items[index], index);
      }
    };
    await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
    return output;
  };

  const directoryFor = async (root, parts, create = false) => {
    let directory = root;
    for (const part of parts) directory = await directory.getDirectoryHandle(part, { create });
    return directory;
  };

  const writeFile = async (root, path, content) => {
    const parts = path.split("/");
    const filename = parts.pop();
    const directory = await directoryFor(root, parts, true);
    const handle = await directory.getFileHandle(filename, { create: true });
    const writable = await handle.createWritable();
    await writable.write(content);
    await writable.close();
  };

  const readJson = async (root, path) => {
    try {
      const parts = path.split("/");
      const filename = parts.pop();
      const directory = await directoryFor(root, parts);
      const handle = await directory.getFileHandle(filename);
      return JSON.parse(await (await handle.getFile()).text());
    } catch (error) {
      if (error.name === "NotFoundError" || error instanceof SyntaxError) return;
      throw error;
    }
  };

  const validConversation = async (root, path, uuid) => {
    const value = await readJson(root, path);
    return value?.uuid === uuid && Array.isArray(value.chat_messages);
  };

  const make = (tag, properties = {}, children = []) => {
    const node = document.createElement(tag);
    Object.assign(node, properties);
    node.append(...children);
    return node;
  };

  const panel = make("section", { id: panelId });
  Object.assign(panel.style, {
    position: "fixed",
    zIndex: "2147483647",
    right: "24px",
    top: "24px",
    width: "390px",
    padding: "18px",
    border: "1px solid #7775",
    borderRadius: "14px",
    background: "#f7f5ef",
    color: "#24221f",
    boxShadow: "0 12px 40px #0005",
    font: "14px/1.4 system-ui, sans-serif",
  });

  const title = make("strong", { textContent: "Claude chat exporter" });
  const close = make("button", { textContent: "Close", type: "button" });
  const heading = make("div", {}, [title, close]);
  Object.assign(heading.style, { display: "flex", justifyContent: "space-between", alignItems: "center" });
  close.onclick = () => panel.remove();

  const note = make("p", {
    textContent: "Writes conversations as they arrive. Select the same folder again to resume, skip unchanged files, and retry failures.",
  });
  const organization = make("select");
  const scope = make("select", {}, [
    make("option", { value: "all", textContent: "All conversations" }),
    make("option", { value: "project", textContent: "Current project" }),
    make("option", { value: "chat", textContent: "Current conversation" }),
  ]);

  const controls = make("div", {}, [organization, scope]);
  Object.assign(controls.style, { display: "grid", gap: "8px" });
  for (const select of [organization, scope]) Object.assign(select.style, { width: "100%", padding: "8px" });

  const exportButton = make("button", { type: "button", textContent: "Choose folder and export", disabled: true });
  Object.assign(exportButton.style, { padding: "8px 11px", marginTop: "12px", cursor: "pointer" });
  Object.assign(close.style, { padding: "7px 10px", cursor: "pointer" });

  const status = make("pre", { textContent: "Loading organizations..." });
  Object.assign(status.style, { whiteSpace: "pre-wrap", maxHeight: "210px", overflow: "auto", marginBottom: 0 });
  panel.append(heading, note, controls, exportButton, status);
  document.body.append(panel);

  const setStatus = message => status.textContent = message;
  const setBusy = busy => {
    exportButton.disabled = busy || !("showDirectoryPicker" in window);
    organization.disabled = busy;
    scope.disabled = busy;
  };

  const detailPath = (orgUuid, chatUuid) => `/api/organizations/${orgUuid}/chat_conversations/${chatUuid}?tree=True&rendering_mode=messages&render_all_tools=true&consistency=strong`;

  const inferOrganization = async organizations => {
    const probe = visibleChatUuid
      ? uuid => detailPath(uuid, visibleChatUuid)
      : visibleProjectUuid
        ? uuid => `/api/organizations/${uuid}/projects/${visibleProjectUuid}`
        : null;
    if (!probe) return;
    for (const item of organizations) {
      try {
        await api(probe(item.uuid));
        organization.value = item.uuid;
        return item;
      } catch {}
    }
  };

  const organizationsReady = api("/api/organizations").then(async result => {
    const organizations = rows(result);
    if (!organizations.length) throw new Error("No Claude organizations were returned.");
    for (const item of organizations) {
      organization.append(make("option", {
        value: item.uuid,
        textContent: `${item.name || item.display_name || "Organization"} (${item.uuid.slice(0, 8)})`,
      }));
    }
    const inferred = await inferOrganization(organizations);
    setBusy(false);
    setStatus(inferred ? `Ready. Selected ${inferred.name || inferred.display_name || inferred.uuid}.` : "Ready. Choose the organization that owns the chats.");
    if (!("showDirectoryPicker" in window)) setStatus("This browser does not support folder access.");
    return organizations;
  }).catch(error => {
    setStatus(`Could not load organizations:\n${error.message}`);
    throw error;
  });

  const listProjectChats = async (orgUuid, projectUuid) => {
    const output = [];
    for (let offset = 0; ; offset += pageLimit) {
      const result = await api(`/api/organizations/${orgUuid}/projects/${projectUuid}/conversations_v2?limit=${pageLimit}&offset=${offset}`);
      const page = rows(result);
      output.push(...page);
      if (result?.pagination ? !result.pagination.has_more : page.length < pageLimit) return output;
    }
  };

  const listAllChats = async orgUuid => {
    const output = [];
    for (let offset = 0; ; offset += pageLimit) {
      const result = await api(`/api/organizations/${orgUuid}/chat_conversations?limit=${pageLimit}&offset=${offset}&consistency=strong`);
      const page = rows(result);
      output.push(...page);
      if (result?.pagination ? !result.pagination.has_more : page.length < pageLimit) return output;
    }
  };

  const prepare = async (orgUuid, selectedScope) => {
    let projectUuid = currentProjectUuid;
    let currentChat;
    let chatList;

    if (selectedScope === "chat") {
      if (!currentChatUuid) throw new Error("Open a Claude conversation before using the current-conversation scope.");
      currentChat = await api(detailPath(orgUuid, currentChatUuid));
      projectUuid = currentChat.project_uuid;
      chatList = [currentChat];
    } else if (selectedScope === "project") {
      if (!projectUuid && currentChatUuid) {
        currentChat = await api(detailPath(orgUuid, currentChatUuid));
        projectUuid = currentChat.project_uuid;
      }
      if (!projectUuid) throw new Error("The current conversation does not belong to a project.");
      chatList = await listProjectChats(orgUuid, projectUuid);
    } else {
      chatList = await listAllChats(orgUuid);
    }

    let projects = [];
    let projectMetadataWarning = null;
    try {
      projects = rows(await api(`/api/organizations/${orgUuid}/projects?include_harmony_projects=true&limit=${pageLimit}`));
    } catch (error) {
      projectMetadataWarning = error.message;
    }
    if (projectUuid && !projects.some(item => item.uuid === projectUuid)) {
      try {
        projects.push(await api(`/api/organizations/${orgUuid}/projects/${projectUuid}`));
      } catch (error) {
        projectMetadataWarning ||= error.message;
      }
    }
    return { chatList, currentChat, projectUuid, projects, projectMetadataWarning };
  };

  const exportTo = async chosenDirectory => {
    await organizationsReady;
    const orgUuid = organization.value;
    const selectedScope = scope.value;
    const rootName = `claude-export-${orgUuid}`;
    const root = chosenDirectory.name === rootName
      ? chosenDirectory
      : await chosenDirectory.getDirectoryHandle(rootName, { create: true });
    const previous = await readJson(root, "export-state.json");
    const state = previous?.format === "claude-chat-export-state-v2" ? previous : {
      format: "claude-chat-export-state-v2",
      organization_uuid: orgUuid,
      created_at: now(),
      conversations: {},
      projects: {},
      errors: {},
    };
    state.last_run_started_at = now();
    state.last_run_scope = selectedScope;

    let saveQueue = Promise.resolve();
    const saveState = () => {
      const snapshot = json(state);
      saveQueue = saveQueue.then(() => writeFile(root, "export-state.json", snapshot));
      return saveQueue;
    };
    await saveState();

    setStatus("Reading conversation indexes...");
    const prepared = await prepare(orgUuid, selectedScope);
    const unique = [...new Map(prepared.chatList.map(item => [item.uuid, item])).values()];
    const projectByUuid = new Map(prepared.projects.map(item => [item.uuid, item]));
    for (const conversation of unique) {
      const uuid = conversation.project_uuid;
      if (uuid && !projectByUuid.has(uuid)) projectByUuid.set(uuid, { uuid, name: "project", metadata_unavailable: true });
    }

    const includedProjects = selectedScope === "all"
      ? [...projectByUuid.values()]
      : [...projectByUuid.values()].filter(item => item.uuid === prepared.projectUuid);
    await writeFile(root, "projects.json", json(includedProjects));
    for (const project of includedProjects) await writeFile(root, `projects/${project.uuid}/project.json`, json(project));

    const groups = new Map();
    for (const conversation of unique) {
      const key = conversation.project_uuid || "unfiled";
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(conversation);
    }

    let exported = 0;
    let skipped = 0;
    let failed = 0;
    const total = unique.length;
    const progress = label => setStatus([
      `Project group: ${label}`,
      `Conversations: ${exported + skipped + failed}/${total}`,
      `Written: ${exported}  Unchanged: ${skipped}  Failed: ${failed}`,
      "You can close the tab and run the exporter again to resume.",
    ].join("\n"));

    const processGroup = async ([projectKey, conversations]) => {
      const base = projectKey === "unfiled" ? "unfiled-conversations" : `projects/${projectKey}`;
      await writeFile(root, `${base}/index.json`, json(conversations));
      state.projects[projectKey] = {
        status: "running",
        conversation_count: conversations.length,
        started_at: now(),
      };
      await saveState();

      await pool(conversations, chatConcurrency, async metadata => {
        const path = `${base}/conversations/${metadata.uuid}.json`;
        const completed = state.conversations[metadata.uuid];
        if (completed?.updated_at === metadata.updated_at && await validConversation(root, completed.path, metadata.uuid)) {
          skipped++;
          progress(projectKey);
          return;
        }
        try {
          const conversation = prepared.currentChat?.uuid === metadata.uuid
            ? prepared.currentChat
            : await api(detailPath(orgUuid, metadata.uuid));
          await writeFile(root, path, json(conversation));
          state.conversations[metadata.uuid] = {
            path,
            updated_at: conversation.updated_at || metadata.updated_at,
            exported_at: now(),
          };
          delete state.errors[metadata.uuid];
          exported++;
        } catch (error) {
          state.errors[metadata.uuid] = {
            name: metadata.name || "",
            error: error.message,
            failed_at: now(),
          };
          failed++;
        }
        await saveState();
        progress(projectKey);
      });

      state.projects[projectKey] = {
        ...state.projects[projectKey],
        status: "complete",
        finished_at: now(),
      };
      await saveState();
    };

    progress("starting");
    await pool([...groups.entries()], projectConcurrency, processGroup);
    state.last_run_finished_at = now();
    state.last_run = { total, exported, skipped, failed };
    await saveState();
    await saveQueue;

    const manifest = {
      format: "claude-chat-export-v2",
      exported_at: state.last_run_finished_at,
      organization_uuid: orgUuid,
      scope: selectedScope,
      project_uuid: selectedScope === "all" ? null : prepared.projectUuid,
      conversation_count: total,
      project_count: includedProjects.length,
      written_this_run: exported,
      unchanged_this_run: skipped,
      failed_this_run: failed,
      project_metadata_warning: prepared.projectMetadataWarning,
      source: location.href,
    };
    await writeFile(root, "manifest.json", json(manifest));
    setStatus(`Done. Wrote ${exported}, skipped ${skipped}, failed ${failed}.\nResume directory: claude-export-${orgUuid}`);
  };

  exportButton.onclick = async () => {
    try {
      const directory = await window.showDirectoryPicker({
        id: "claude-chat-export",
        mode: "readwrite",
        startIn: "downloads",
      });
      setBusy(true);
      await exportTo(directory);
    } catch (error) {
      if (error.name !== "AbortError") setStatus(`Export failed:\n${error.stack || error.message}`);
    } finally {
      setBusy(false);
    }
  };
})();
