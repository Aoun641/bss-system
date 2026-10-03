async function deleteStudent(id, name) {
    if (!confirm(`Are you sure you want to delete student: ${name}?`)) return;
    try {
        const res = await fetch(`/api/student/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) { alert('Deleted successfully'); window.location.reload(); }
        else { alert(data.error || 'Failed to delete'); }
    } catch (e) { alert('Server error'); }
}

async function deleteTeacher(id, name) {
    if (!confirm(`Are you sure you want to delete teacher: ${name}?`)) return;
    try {
        const res = await fetch(`/api/teacher/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) { alert('Deleted successfully'); window.location.reload(); }
        else { alert(data.error || 'Failed to delete'); }
    } catch (e) { alert('Server error'); }
}