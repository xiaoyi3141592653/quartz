import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer(),
}

export const sortFn: Options["sortFn"] = (a, b) => {
  if ((!a.isFolder && !b.isFolder) || (a.isFolder && b.isFolder)) {
    if (a.data.filePath == "最近更新.md") {
      return -1
    } else if (b.data.filePath == "最近更新.md") {
      return 1
    }
    let compare_date = function(aa, bb) {
      return new Date(bb.data.date).getTime() - new Date(aa.data.date).getTime();
    }
    if (a.data.date && b.data.date) {
      return compare_date(a, b)
    }
    return a.displayName.localeCompare(b.displayName, undefined, {
      numeric: true,
      sensitivity: "base",
    })
  }

  if (!a.isFolder && b.isFolder) {
    return 1
  } else {
    return -1
  }
}

export const mapFn: Options["mapFn"] = (node) => {
  if (node.isFolder) {
    node.displayName = "📁 " + node.displayName
  } else {
    let file_date = new Date(node.data.date ?? Date.now());
    const year = file_date.getFullYear();
    const month = String(file_date.getMonth() + 1).padStart(2, '0'); // 月份从0开始需+1
    const day = String(file_date.getDate()).padStart(2, '0');
    const hours = String(file_date.getHours()).padStart(2, '0');
    const minutes = String(file_date.getMinutes()).padStart(2, '0');
    let display_date =  `${year}-${month}-${day} ${hours}:${minutes}`;
    if (node.displayName == "最近更新") {
      node.displayName = `🔥 [${display_date}] 最近更新`
    } else {
      node.displayName = `📄 [${display_date}] ${node.displayName}`
    }
  }
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    Component.Explorer(
      {
        mapFn,
        sortFn
      }
    ),
  ],
  right: [
    Component.Graph(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ]
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer(
      {
        mapFn,
        sortFn
      }
    ),
  ],
  right: []
}
