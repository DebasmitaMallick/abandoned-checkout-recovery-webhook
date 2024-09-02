const HEADERS = [
  "Customer Name",
  "Email",
  "Message",
  "Message Sent At",
  "Order Status",
  "Order Created At",
];

const getFormattedDateTime = (dateTimeString) => {
  if (dateTimeString === "") return dateTimeString;

  // Convert the string into a Date object
  const date = new Date(dateTimeString);

  // Format both date and time together
  const formattedDateTime = date.toLocaleString("en-US", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false, // Use true for 12-hour format with AM/PM
  });

  return formattedDateTime; // Output: 09/02/2024, 08:52:51
};
export function DataTable({ data }) {
  return (
    <div className="relative overflow-x-auto">
      <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            {HEADERS.map((header) => (
              <th key={header} scope="col" className="px-6 py-3">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((data) => {
            const rowData = {
              "Customer Name": (
                <span className="inline-block text-nowrap font-medium">
                  {data.customer_name}
                </span>
              ),
              Email: <span className="text-blue-600">{data.email}</span>,
              Message: <span>{data.message}</span>,
              "Message Sent At": (
                <span>{getFormattedDateTime(data.message_sent_at || "")}</span>
              ),
              "Order Status": data.order_id ? (
                <span className="text-green-500 font-bold">Completed</span>
              ) : (
                <span className="text-orange-500 font-bold">Pending</span>
              ),
              "Order Created At": (
                <span>{getFormattedDateTime(data.order_created_at || "")}</span>
              ),
            };
            return (
              <tr
                key={data.message_id}
                className="bg-white border-b dark:bg-gray-800 dark:border-gray-700"
              >
                {Object.keys(rowData).map((objKey) => (
                  <td key={objKey} className="px-6 py-4">
                    {rowData[objKey]}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
