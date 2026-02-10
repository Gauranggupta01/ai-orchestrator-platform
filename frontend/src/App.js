import { useState } from "react";
import ReactMarkdown from "react-markdown";

function App() {
  const [prompt, setPrompt] = useState("");
  const [type, setType] = useState("text");

  const [reply, setReply] = useState("");
  const [replyType, setReplyType] = useState("text");

  const [loading, setLoading] = useState(false);

  const sendPrompt = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setReply("");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/generate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
          type: type,
        }),
      });

      const data = await res.json();

      setReply(data.result);
      setReplyType(data.result_type); // ✅ important fix
    } catch (error) {
      setReply("❌ Error: Backend not responding");
      setReplyType("text");
    }

    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>AI Multi-Mode Generator</h1>

        {/* Prompt Input */}
        <input
          style={styles.input}
          type="text"
          value={prompt}
          placeholder="Enter your prompt..."
          onChange={(e) => setPrompt(e.target.value)}
        />

        {/* Mode Selector */}
        <select
          style={styles.select}
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="text">Text Answer</option>
          <option value="code">Code Assistant</option>
          <option value="summary">Summarize</option>
          <option value="image">Image Generate</option>
        </select>

        {/* Button */}
        <button
          style={{
            ...styles.button,
            opacity: loading ? 0.7 : 1,
          }}
          onClick={sendPrompt}
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate"}
        </button>

        {/* Output Box */}
        <div style={styles.outputBox}>
          <h3 style={styles.outputTitle}>Response:</h3>

          {loading ? (
            <p style={styles.loadingText}>AI is thinking...</p>
          ) : reply ? (
            replyType === "image" ? (
              <div style={styles.imageBox}>
                <img
                  src={reply}
                  alt="Generated AI"
                  style={styles.generatedImage}
                />
              </div>
            ) : (
              <div style={styles.markdown}>
                <ReactMarkdown
                  components={{
                    code({ children }) {
                      return (
                        <pre style={styles.codeBlock}>
                          <code>{children}</code>
                        </pre>
                      );
                    },
                  }}
                >
                  {reply}
                </ReactMarkdown>
              </div>
            )
          ) : (
            <p style={styles.placeholder}>Output will appear here...</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
    paddingTop: "40px",
    paddingBottom: "40px",
    background: "#f5f7fb",
    fontFamily: "Arial, sans-serif",
    overflowY: "auto",
  },

  card: {
    width: "90%",
    maxWidth: "650px",
    padding: "35px",
    borderRadius: "18px",
    background: "white",
    boxShadow: "0px 8px 25px rgba(0,0,0,0.15)",
    textAlign: "center",
  },

  title: {
    fontSize: "30px",
    marginBottom: "25px",
    fontWeight: "bold",
    color: "#1e293b",
  },

  input: {
    width: "100%",
    padding: "14px",
    fontSize: "16px",
    borderRadius: "10px",
    border: "1px solid #cbd5e1",
    outline: "none",
    marginBottom: "15px",
  },

  select: {
    width: "100%",
    padding: "12px",
    fontSize: "16px",
    borderRadius: "10px",
    border: "1px solid #cbd5e1",
    marginBottom: "20px",
    outline: "none",
  },

  button: {
    width: "100%",
    padding: "14px",
    fontSize: "16px",
    borderRadius: "10px",
    border: "none",
    background: "#2563eb",
    color: "white",
    cursor: "pointer",
    fontWeight: "bold",
  },

  outputBox: {
    marginTop: "30px",
    padding: "20px",
    borderRadius: "12px",
    background: "#f8fafc",
    height: "350px",
    overflowY: "auto",
    textAlign: "left",
    border: "1px solid #e2e8f0",
  },

  outputTitle: {
    marginBottom: "12px",
    fontSize: "18px",
    fontWeight: "bold",
    color: "#0f172a",
  },

  loadingText: {
    fontStyle: "italic",
    color: "#64748b",
  },

  placeholder: {
    color: "#94a3b8",
    fontStyle: "italic",
  },

  markdown: {
    fontSize: "15px",
    lineHeight: "1.7",
    color: "#1e293b",
    wordWrap: "break-word",
    overflowWrap: "break-word",
  },

  codeBlock: {
    background: "#0f172a",
    color: "white",
    padding: "12px",
    borderRadius: "10px",
    overflowX: "auto",
  },

  imageBox: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },

  generatedImage: {
    width: "100%",
    maxHeight: "320px",
    objectFit: "contain",
    borderRadius: "12px",
    border: "1px solid #cbd5e1",
  },
};
