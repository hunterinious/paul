$(document).ready(function(){

    let pay_form = document.getElementById("pay-form")
    let submit_button = document.getElementById("submit-button")
    let url = "api.semantic-portal.net/paul/"

    function isNumber(str) {
      if (typeof str != "string") return false

      return !isNaN(str) && !isNaN(parseFloat(str))
    }


    pay_form.addEventListener('submit', function(evt){

       let sel_cur = document.getElementById("select-currency")
       let cur_amount = document.getElementById("currency-amount")
       let cur_amount_val = cur_amount.value
       let currency = sel_cur.options[sel_cur.selectedIndex].value


       if (!isNumber(cur_amount_val) ) {
            evt.preventDefault();
            alert("Вы неверно указали сумму оплаты")
       }

       if(currency != 978) {
            let form = document.getElementById('pay-form');
            let input = document.createElement('input');
            if(currency == 643){
                input.name = 'payway'
                input.value = 'payeer_rub'
                input.type = 'hidden'
                form.appendChild(input)
                action = $("#pay-form").attr("action", "pay_rub")
            } else if(currency ==  840){
                input.name = 'payer_currency'
                currencyValues = ['978', '840', '643']
                randomIndex = Math.floor(Math.random() * currencyValues.length)
                input.value = currencyValues[randomIndex]
                input.type = 'hidden'
                sel_cur.name = 'shop_currency'
                cur_amount.name = 'shop_amount'
                form.appendChild(input)
                action = $("#pay-form").attr("action", "pay_usd")
            }

       } else{
           amount = $("input[name='amount']").val()
           shop_id = $("input[name='shop_id']").val()
           shop_order_id = $("input[name='shop_order_id']").val()
           description = $("#description-area").val()

           let new_data = {
                "amount": amount,
                "currency": currency,
                "shop_id": shop_id,
                "shop_order_id": shop_order_id,
                "description": description
           }

           $.ajax({
                type:'POST',
                contentType: "application/json",
                async: false,
                url: "pay_eur",
                data: JSON.stringify(new_data),
                dataType: "json",
                success:function(data) {

                    $("#sign").val(data["sign"])
                    $("#shop_order_id").val(data["shop_order_id"])
                },
                error: function (request, status, error) {
//                     alert(request.responseText);
                }
           });

       }
    }, false)

});
