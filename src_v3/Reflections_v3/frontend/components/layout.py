from fasthtml.common import *

# This is your main site layout.
# All other pages will be wrapped in this.
def PageLayout(title: str, *content):
    return Html(
        Head(
            Title(title),
            Style("""
                body {
                    font-family: system-ui, -apple-system, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    display: flex;
                    gap: 20px;
                }
                nav {
                    min-width: 200px;
                    padding: 20px;
                    background: #f5f5f5;
                    border-radius: 8px;
                }
                nav ul {
                    list-style: none;
                    padding: 0;
                }
                nav li {
                    margin: 10px 0;
                }
                nav a {
                    text-decoration: none;
                    color: #0066cc;
                }
                nav a:hover {
                    text-decoration: underline;
                }
                main {
                    flex: 1;
                }
                .card {
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 8px;
                    background: white;
                }
                .card:hover {
                    background: #f9f9f9;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                    max-width: 600px;
                }
                label {
                    font-weight: bold;
                }
                input, textarea, select {
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 14px;
                }
                textarea {
                    min-height: 150px;
                    font-family: inherit;
                }
                button {
                    padding: 10px 20px;
                    background: #0066cc;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                }
                button:hover {
                    background: #0052a3;
                }
                a {
                    color: inherit;
                    text-decoration: none;
                }
            """)
        ),
        Body(
            Div(
                # --- Left Navigation ---
                Nav(
                    H3("Reflection App"),
                    Ul(
                        Li(A("All Reflections", href="/reflections")),
                        Li(A("Add Reflection", href="/reflections/new")),
                    ),
                ),
                
                # --- Main Page Content ---
                Main(
                    *content,
                ),
            )
        )
    )