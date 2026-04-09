const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function sendMessageToAgent(payload) {
  const response = await fetch(`${API_BASE_URL}/api/agent/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error ${response.status}: ${errorText}`);
  }

  return response.json();
}

export async function getDoctorsByDepartment(deptId) {
  const response = await fetch(`${API_BASE_URL}/api/departments/${deptId}/doctors`);
  if (!response.ok) throw new Error(`API error ${response.status}`);
  return response.json();
}

export async function getDoctorSchedule(doctorId, date) {
  const response = await fetch(
    `${API_BASE_URL}/api/doctors/${doctorId}/schedule?date=${date}`
  );
  if (!response.ok) throw new Error(`API error ${response.status}`);
  return response.json();
}

export async function createBooking({ date, time, departmentId, doctorId }) {
  const response = await fetch(`${API_BASE_URL}/api/booking`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      date,
      time,
      department_id: departmentId,
      doctor_id: doctorId,
    }),
  });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error ${response.status}: ${errorText}`);
  }
  return response.json();
}