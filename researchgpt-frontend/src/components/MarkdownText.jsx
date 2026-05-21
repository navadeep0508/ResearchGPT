function parseInline(text) {
  const parts = text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g);

  return parts.map((part, index) => {
    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={index}
          className="rounded bg-slate-100 px-1.5 py-0.5 text-[0.92em] text-slate-800"
        >
          {part.slice(1, -1)}
        </code>
      );
    }

    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }

    return part;
  });
}

export default function MarkdownText({ text = "" }) {
  const lines = String(text).split("\n");
  const blocks = [];
  let listItems = [];

  function flushList() {
    if (listItems.length > 0) {
      blocks.push(
        <ul key={`list-${blocks.length}`} className="my-3 list-disc space-y-1 pl-5">
          {listItems.map((item, index) => (
            <li key={index}>{parseInline(item)}</li>
          ))}
        </ul>
      );
      listItems = [];
    }
  }

  lines.forEach((line, index) => {
    const trimmed = line.trim();

    if (!trimmed) {
      flushList();
      return;
    }

    if (trimmed.startsWith("- ")) {
      listItems.push(trimmed.slice(2));
      return;
    }

    flushList();

    if (trimmed.startsWith("### ")) {
      blocks.push(
        <h3 key={index} className="mt-4 text-base font-semibold text-slate-950">
          {parseInline(trimmed.slice(4))}
        </h3>
      );
      return;
    }

    if (trimmed.startsWith("## ")) {
      blocks.push(
        <h2 key={index} className="mt-4 text-lg font-semibold text-slate-950">
          {parseInline(trimmed.slice(3))}
        </h2>
      );
      return;
    }

    blocks.push(
      <p key={index} className="my-2 leading-7">
        {parseInline(trimmed)}
      </p>
    );
  });

  flushList();

  return <div className="prose-lite text-sm text-slate-700">{blocks}</div>;
}
