// $(document).ready(function (){
//     $(".my_dropdown").each(function (){
//         $(this).change(function (){
//             const category_id = $(this).val();
//             const row = $(this).closest("tr");
//             const channel_name = row.find(".channel-name-input").val();
//             const channel_url = row.find(".channel-url-input").val();
//             const pic_url = row.find(".channel-pic-input").val();
//             const csrf_token =  $("input[name='csrfmiddlewaretoken']").val();
//             if (category_id) {
//                 $.ajax({
//                     type: "POST",
//                     url: "/populate_category/",
//                     data: {
//                         "category_id": category_id,
//                         'channel_name': channel_name,
//                         'channel_url': channel_url,
//                         'pic_url': pic_url,
//                         'csrfmiddlewaretoken': csrf_token
//                     },
//                     success: function (response) {
//                         if (response.status === "success") {
//                             console.log("success")
//                         }
//                     },
//                     error: function (response) {
//                         console.log("error")
//                     }
//                 })
//             }
//         });
//     });
// });


// document.addEventListener('DOMContentLoaded', function(e) {
//     let channelSubmitButton = document.getElementById('submit-channel-form');
//     channelSubmitButton.addEventListener('click', function(e) {
//         let channelForm = document.getElementById('channel-form');
//         HTMX.trigger(form, 'submit');
//     })
// })








