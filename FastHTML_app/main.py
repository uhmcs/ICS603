from fasthtml.common import *
from components.user_row_entry import UserRowEntry

# In-memory "database"
db = []

app, rt = fast_app(
    hdrs=(
        Style("""
            .titled-center h1 {
                text-align: center;
            }
        """),
    )
)

# ---------- First Page ----------
@rt("/")
def get():
    count = len(db)
    return Div(
        Div(   # Card container
            Titled(
                "User Entry",
                Form(
                    Group(
                        Div(
                            Label("First Name", _for="first_name", cls="block mb-1 font-medium"),
                            Input(
                                name="first_name",
                                id="first_name",
                                placeholder="e.g., Jane"
                            )
                        ),
                        Div(
                            Label("Last Name", _for="last_name", cls="block mb-1 font-medium"),
                            Input(
                                name="last_name",
                                id="last_name",
                                placeholder="e.g., Doe"
                            )
                        ),
                    ),
                    Button(
                        "Submit >", 
                        type="submit"
                    ),
                    hx_post="/add",
                    hx_target="#status",
                    hx_swap="outerHTML",
                    hx_on__after_request="this.reset()"   # ✅ clears form after request
                ),
                Hr(cls="my-4"),
                Div(
                    H3("Activity & Status", cls="text-lg font-semibold mb-2"),
                    Div(
                        f"Currently DB contains {count} entries",
                        id="status"
                    )
                ),
                A(
                    "View All Entries", 
                    href="/records"
                ),
                cls="titled-center"
            ),
        )
    )


# ---------- Handle Form Submission ----------
@rt("/add")
def post(first_name: str, last_name: str):
    if first_name and last_name:
        db.append({"first": first_name, "last": last_name})
    return Div(
        f"Currently DB contains {len(db)} entries",
        id="status"
    )


# ---------- Delete User ----------
@rt("/delete/{index}")
def delete(index: int):
    if 0 <= index < len(db):
        db.pop(index)
    # Return empty string to remove the row from the DOM
    return ""


# ---------- Second Page ----------
@rt("/records")
def get():
    table = Table(
        Thead(
            Tr(
                Th("FIRST NAME", cls="px-4 py-2 text-left border-b"),
                Th("LAST NAME", cls="px-4 py-2 text-left border-b"),
                Th("ACTION", cls="px-4 py-2 text-center border-b"),
            )
        ),
        Tbody(
            *[UserRowEntry(user, idx) for idx, user in enumerate(db)]
        )
    )
    return Div(
        Div(
            Titled(
                "User Records",
                table if db else P("No records found. Add some users first!", cls="text-gray-500 italic"),
                A(
                    "< Back to Input", 
                    href="/"
                ),
                cls="titled-center"
            ),
        )
    )

if __name__ == "__main__":
    serve()