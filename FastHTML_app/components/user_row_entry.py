from fasthtml.common import *

def UserRowEntry(user, index):
    """
    Component for rendering a single user row with delete functionality.
    
    Args:
        user: Dictionary with 'first' and 'last' keys
        index: The index of the user in the database
    """
    return Tr(
        Td(user["first"], cls="px-4 py-2 border-b"),
        Td(user["last"], cls="px-4 py-2 border-b"),
        Td(
            Button(
                "X",
                hx_delete=f"/delete/{index}",
                hx_target="closest tr",
                hx_swap="outerHTML swap:0.5s",
                cls="text-red-600 hover:text-red-800 font-bold px-2"
            ),
            cls="px-4 py-2 border-b text-center"
        ),
        id=f"user-row-{index}"
    )