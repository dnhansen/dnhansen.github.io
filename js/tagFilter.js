const activeTags = new Set();
/**
   * @returns A list of strings containing the values of the `tags` field
   * of the URL query string, formatted as a comma-separated list.
   */
function getTagsFromUrl() {
    var _a;
    const params = new URLSearchParams(window.location.search);
    return ((_a = params
        .get("tags")) === null || _a === void 0 ? void 0 : _a.split(",").filter(Boolean) // Removes empty items, not sure if necessary
    )
        || [];
}
// Overwrites the entire query string, but not the path it seems. TODO understand History API
/**
   * Replaces the value of the `tags` field of the URL query string with the contents of
   * the global array `activeTags`.
   */
function updateUrl() {
    const params = new URLSearchParams();
    if (activeTags.size) {
        params.set("tags", [...activeTags].join(","));
        history.replaceState(null, "", "?" + params.toString());
    }
    else {
        history.replaceState(null, "", window.location.pathname);
    }
}
/**
   * Updates the sidebar checkboxes to reflect the contents of the global array `activeTags`.
   */
function updateSidebar() {
    const checkboxes = document.querySelectorAll("input[data-tag]");
    checkboxes.forEach(elem => {
        const tag = elem.dataset.tag;
        elem.classList.toggle("active", activeTags.has(tag));
        elem.checked = activeTags.has(tag);
    });
}
/**
   * Filters the post list according to the tags in the global array `activeTags`.
   */
function updatePostList() {
    const posts = document.querySelectorAll("article[data-tags]");
    posts.forEach(post => {
        const postTags = new Set(post.dataset.tags.split(","));
        const visible = [...activeTags].every(tag => postTags.has(tag));
        post.style.display = visible ? "" : "none";
    });
}
/**
   * Updates the UI to reflect the tags in the global array `activeTags`.
   *
   * @see the functions `updateSidebar` and `updatePostList`, which this function calls.
   */
function updateUi() {
    updateSidebar();
    updatePostList();
}
/**
   * Toggles the argument `tag` in the global array `activeTags`.
   *
   * @param tag - The tag to toggle.
   */
function toggleTag(tag) {
    if (activeTags.has(tag)) {
        activeTags.delete(tag);
    }
    else {
        activeTags.add(tag);
    }
}
/**
   * Checks whether an element is of type `TagFilter`.
   *
   * @param elem - The element to check
   * @returns Whether the element is of type `TagFilter` or not.
   */
function isTagFilter(elem) {
    return elem.dataset.tag !== undefined;
}
/**
   * Handles click events.
   *
   * @param e - The event to handle.
   */
function handleClick(e) {
    if (!e.target)
        return;
    if (!(e.target instanceof Element))
        return;
    const elem = e.target.closest("input[data-tag], button[data-tag], button[data-action]");
    if (!elem)
        return;
    // e.preventDefault(); // TODO understand when this makes sense
    // Handle tag toggle or replace
    if (isTagFilter(elem)) {
        const tag = elem.dataset.tag;
        if (elem.closest(".post-tags")) {
            // Clicked on tag in post
            activeTags.clear();
            activeTags.add(tag);
        }
        else {
            // Clicked on tag in sidebar
            toggleTag(tag);
        }
        updateUrl();
        updateUi();
    }
    else {
        // Handle reset action
        activeTags.clear();
        updateUrl();
        updateUi();
        return;
    }
}
/**
   * Reads the `tags` field of the URL query string and updates the global
   * array `activeTags` with its value. Updates the UI according to these tags.
   * Adds event listener which listens for clicks.
   *
   * @see the functions `updateUi` and `handleClick`, which it calls.
   */
export function init() {
    // TODO should I clear activeTags first for good measure?
    getTagsFromUrl().forEach(tag => activeTags.add(tag));
    updateUi();
    document.addEventListener("click", handleClick);
}
